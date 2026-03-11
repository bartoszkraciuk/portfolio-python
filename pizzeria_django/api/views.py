from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from menu_app.models import Pizza
from .serializers import PizzaSerializer


@api_view(['GET', 'POST'])
def pizza_list_api(request):
    """
    GET  /api/pizzas/ - lista wszystkich pizz
    POST /api/pizzas/ - dodaj nowa pizze
    """
    if request.method == 'GET':
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pizza_detail_api(request, name):
    """
    GET    /api/pizzas/<name>/ - szczegoly pizzy
    PUT    /api/pizzas/<name>/ - aktualizuj pizze
    DELETE /api/pizzas/<name>/ - usun pizze
    """
    try:
        pizza = Pizza.objects.get(name=name)
    except Pizza.DoesNotExist:
        return Response(
            {"error": f"Pizza '{name}' nie znaleziona"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = PizzaSerializer(pizza)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PizzaSerializer(pizza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pizza.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)