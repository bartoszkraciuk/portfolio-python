import os
from django.http import Http404
from django.shortcuts import render, redirect
from pizzeria_engine import DATA_DIR
from pizzeria_engine.pizza import Menu, Pizza
from pizzeria_engine.exceptions import PizzaNotFoundError, InvalidPriceError, DuplicatePizzaError
from django.contrib import messages
from django.shortcuts import render
from .models import Pizza
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Avg

MENU_FILE = os.path.join(DATA_DIR, 'menu.json')

def pizza_list(request):
    sort_by = request.GET.get('sort', 'name')
    pizzas = Pizza.objects.all()

    if sort_by == 'price_asc':
        pizzas = pizzas.order_by('price')
    elif sort_by == 'price_desc':
        pizzas = pizzas.order_by('-price')
    else:
        pizzas = pizzas.order_by('name')

    # Statystyki
    cheapest = Pizza.objects.order_by('price').first()
    most_expensive = Pizza.objects.order_by('-price').first()
    avg_price = Pizza.objects.aggregate(Avg('price'))['price__avg']

    return render(request, 'menu_app/pizza_list.html', {
        'pizzas': pizzas,
        'cheapest': cheapest,
        'most_expensive': most_expensive,
        'avg_price': avg_price,
    })

def pizza_detail(request, name):
    pizzas = Pizza.objects.all()
    try:
        pizza = Pizza.objects.get(name=name)
    except Pizza.DoesNotExist:
        raise Http404(f"Pizza '{name}' nie znaleziona")
    return render(request, 'menu_app/pizza_detail.html', {'pizza': pizza})

def pizza_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price_str = request.POST.get('price', '').strip()

        errors = []
        if not name:
            errors.append("Nazwa pizzy jest wymagana.")
        if not price_str:
            errors.append("Cena jest wymagana.")

        if not errors:
            try:
                price = float(price_str)
                Pizza.objects.create(name=name, price=price)
                messages.success(request, f"Dodano pizzę: {name}")
                return redirect('pizza_list')
            except (ValueError, TypeError):
                errors.append("Nieprawidlowa cena.")
            except ValidationError as e:
                errors.extend(e.messages)
            except IntegrityError:
                errors.append(f"Pizza '{name}' juz istnieje!")

        return render(request, 'menu_app/pizza_form.html', {
            'errors': errors,
            'name': name,
            'price': price_str,
        })

    return render(request, 'menu_app/pizza_form.html')

def pizza_delete(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            pizza = Pizza.objects.get(name=name)
            pizza.delete()
            messages.warning(request, f"Pizza '{name}' została usunięta z menu.")
        except Pizza.DoesNotExist:
            messages.warning(request, f"Błąd: Pizza '{name}' nie istnieje.")
    return redirect('pizza_list')