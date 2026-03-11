from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("<h1>Witaj w Pizzerii!</h1>")

def book_list(request):
    books = [
        {'title': 'Python Crash Course', 'author': 'Eric Matthes'},
        {'title': "Fluent Python", 'author': 'Luciano Ramalho'},
        {'title': "Fluent Python3", 'author': 'Luciano Ramalho'},
    ]
    x = render(request, 'books/book_list.html', {'books': books})
    print(x)
    return x