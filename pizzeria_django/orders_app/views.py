from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from menu_app.models import Pizza
from customers_app.models import Customer

def order_list(request):
    orders = Order.objects.select_related('customer').prefetch_related('items').all()
    return render(request, 'orders_app/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders_app/order_detail.html', {'order': order})

def order_create(request):
    if request.method == 'POST':
        customer_id_str = request.POST.get('customer_id', '')
        pizza_id_str = request.POST.get('pizza_id', '')
        quantity_str = request.POST.get('quantity', '1')

        errors = []
        customer, pizza, quantity = None, None, None

        try:
            if not customer_id_str:
                errors.append("Wybierz klienta.")
            else:
                customer = Customer.objects.get(pk=int(customer_id_str))

            if not pizza_id_str:
                errors.append("Wybierz pizze.")
            else:
                pizza = Pizza.objects.get(pk=int(pizza_id_str))

            if not quantity_str or int(quantity_str) <= 0:
                errors.append("Ilość musi być dodatnia.")
            else:
                quantity = int(quantity_str)

        except (Customer.DoesNotExist, Pizza.DoesNotExist, ValueError):
            errors.append("Nieprawidłowe dane formularza.")

        if not errors:
            new_order = Order.objects.create(customer=customer)
            OrderItem.objects.create(
                order=new_order,
                pizza=pizza,
                quantity=quantity,
                unit_price=pizza.price
            )
            messages.success(request, f"Dodano nowe zamówienie: #{new_order.id}")
            return redirect('order_detail', order_id=new_order.id)

        customers = Customer.objects.all()
        pizzas = Pizza.objects.all()
        return render(request, 'orders_app/order_form.html', {
            'errors': errors,
            'pizzas': pizzas,
            'customers': customers,
        })

    customers = Customer.objects.all()
    pizzas = Pizza.objects.all()
    return render(request, 'orders_app/order_form.html', {
        'pizzas': pizzas,
        'customers': customers,
    })

@require_POST
def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_id_display = order.id
    order.delete()
    messages.warning(request, f"Zamówienie #{order_id_display} zostało anulowane.")
    return redirect('order_list')