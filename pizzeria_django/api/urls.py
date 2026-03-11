from django.urls import path
from . import views

urlpatterns = [
    path('pizzas/', views.pizza_list_api, name='pizza_list_api'),
    path('pizzas/<str:name>/', views.pizza_detail_api, name='pizza_detail_api'),
]