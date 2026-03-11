from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .models import Customer


def customer_list(request):
    customers = Customer.objects.all().order_by('id')
    return render(request, 'customers_app/customer_list.html', {'customers': customers})

def customer_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        customer_type = request.POST.get('type', 'regular')

        errors = []
        if not name:
            errors.append("Imie klienta jest wymagane.")
        if not phone:
            errors.append("Numer telefonu jest wymagany.")

        if not errors:
            if customer_type == 'vip':
                discount = float(request.POST.get('discount', 10))
                Customer.objects.create(name=name, phone=phone, customer_type='vip', discount_percent=discount)
            else:
                Customer.objects.create(name=name, phone=phone, customer_type='regular')
            
            messages.success(request, f"Dodano Klienta: {name}")
            return redirect('customer_list')

        return render(request, 'customers_app/customer_form.html', {
            'errors': errors,
            'name': name,
            'phone': phone,
        })

    return render(request, 'customers_app/customer_form.html')

def customer_detail(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        raise Http404(f"Klient o ID {customer_id} nie istnieje.")

    if request.method == 'POST':
        try:
            points = int(request.POST.get('points', 0))
            if points > 0:
                customer.loyalty_points += points
                customer.save()
                messages.success(request, f"Dodano {points} punktów lojalnościowych.")
                return redirect('customer_detail', customer_id=customer_id)
            else:
                messages.warning(request, "Liczba punktów musi być dodatnia.")
        except ValueError:
            messages.error(request, "Nieprawidłowa wartość punktów.")

    return render(request, 'customers_app/customer_detail.html', {'customer': customer})