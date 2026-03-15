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
        pizza_ids = request.POST.getlist('pizza_id')
        quantities = request.POST.getlist('quantity')

        errors = []
        customer = None
        valid_items = []

        try:
            if not customer_id_str:
                errors.append("Wybierz klienta.")
            else:
                customer = Customer.objects.get(pk=int(customer_id_str))
        except (Customer.DoesNotExist, ValueError):
            errors.append("Nieprawidłowy klient.")

        if not pizza_ids or not quantities:
            errors.append("Zamówienie musi zawierać przynajmniej jedną pozycję.")
        elif len(pizza_ids) != len(quantities):
            errors.append("Niezgodna liczba wybranych pizz i ilości.")
        else:
            for p_id_str, q_str in zip(pizza_ids, quantities):
                try:
                    if not p_id_str:
                        errors.append("Wybierz pizzę dla każdej pozycji.")
                        continue
                    
                    pizza = Pizza.objects.get(pk=int(p_id_str))
                    quantity = int(q_str)
                    if quantity <= 0:
                        errors.append(f"Ilość dla {pizza.name} musi być dodatnia.")
                    else:
                        valid_items.append((pizza, quantity))
                except (Pizza.DoesNotExist, ValueError):
                    errors.append("Wybrano nieprawidłową pizzę lub podano złą ilość.")

        # Pozbywamy się ewentualnych zduplikowanych komunikatów o błędach
        errors = list(dict.fromkeys(errors))

        if not errors and valid_items:
            new_order = Order.objects.create(customer=customer)
            for pizza, quantity in valid_items:
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