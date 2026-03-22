from django.shortcuts import render

def index(request):
    return render(request, 'menu/index.html')

def register(request):
    return render(request, 'menu/register.html')