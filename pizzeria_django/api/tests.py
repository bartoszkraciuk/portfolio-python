from django.test import TestCase

# Create your tests here.

import pytest
from rest_framework.test import APIClient
from menu_app.models import Pizza


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_pizza():
    return Pizza.objects.create(name="Margherita", price=25.0)


# === Testy Pizza API ===

class TestPizzaAPI:

    @pytest.mark.django_db
    def test_list_empty(self, api_client):
        """GET /api/pizzas/ zwraca pusta liste gdy brak pizz."""
        response = api_client.get('/api/pizzas/')
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.django_db
    def test_list_with_data(self, api_client, sample_pizza):
        """GET /api/pizzas/ zwraca liste pizz."""
        response = api_client.get('/api/pizzas/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Margherita'

    @pytest.mark.django_db
    def test_detail(self, api_client, sample_pizza):
        """GET /api/pizzas/<name>/ zwraca szczegoly pizzy."""
        response = api_client.get('/api/pizzas/Margherita/')
        assert response.status_code == 200
        assert response.data['name'] == 'Margherita'
        assert response.data['price'] == 25.0

    @pytest.mark.django_db
    def test_detail_not_found(self, api_client):
        """GET /api/pizzas/<name>/ zwraca 404 dla nieistniejacej pizzy."""
        response = api_client.get('/api/pizzas/NieIstniejaca/')
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_create(self, api_client):
        """POST /api/pizzas/ tworzy nowa pizze."""
        response = api_client.post('/api/pizzas/', {
            'name': 'Diavola',
            'price': 34.0,
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Diavola'
        assert Pizza.objects.count() == 1

    @pytest.mark.django_db
    def test_create_invalid(self, api_client):
        """POST /api/pizzas/ z blednymi danymi zwraca 400."""
        response = api_client.post('/api/pizzas/', {
            'name': '',
            'price': 34.0,
        }, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_duplicate(self, api_client, sample_pizza):
        """POST /api/pizzas/ z duplikatem nazwy zwraca 400."""
        response = api_client.post('/api/pizzas/', {
            'name': 'Margherita',
            'price': 99.0,
        }, format='json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update(self, api_client, sample_pizza):
        """PUT /api/pizzas/<name>/ aktualizuje pizze."""
        response = api_client.put('/api/pizzas/Margherita/', {
            'name': 'Margherita',
            'price': 28.0,
        }, format='json')
        assert response.status_code == 200
        assert response.data['price'] == 28.0

    @pytest.mark.django_db
    def test_delete(self, api_client, sample_pizza):
        """DELETE /api/pizzas/<name>/ usuwa pizze."""
        response = api_client.delete('/api/pizzas/Margherita/')
        assert response.status_code == 204
        assert Pizza.objects.count() == 0