from rest_framework import serializers
from menu_app.models import Pizza


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['name', 'price']