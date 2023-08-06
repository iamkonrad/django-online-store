import pytest
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import JsonResponse
from store.models import Product
from .cart import Cart


class TestCartViews(TestCase):

    @pytest.fixture
    def setup(self):
        self.product = Product.objects.create(name="Havana Shirt", price=125)


    @pytest.mark.django_db
    def test_cart_summary(self):
        browser = Client()
        response = self.client.get(reverse('cart_summary'))
        assert response.status_code == 200
        assert 'cart' in response.context

    @pytest.mark.django_db
    def test_cart_add(self, setup):
        browser = Client()
        url = reverse('cart_add')
        response = self.client.post(url, {'action': 'post', 'product_id': self.product.id, 'product_quantity': 3})
        assert response.status_code == 200
        assert response.json()['qty'] == 3  # Assuming the cart was initially empty

    @pytest.mark.django_db
    def test_cart_delete(self, setup):
        browser = Client()
        url = reverse('cart_delete')
        response = self.client.post(url, {'action': 'post', 'product_id': self.product.id})
        assert response.status_code == 200
        assert response.json()['qty'] == 0  # Assuming the cart had one item and it was deleted

    @pytest.mark.django_db
    def test_cart_delete(self, setup):
        browser = Client()
        # Add both products to the cart
        url_add = reverse('cart_add')
        response_add_1 = self.client.post(url_add,
                                          {'action': 'post', 'product_id': self.product1.id, 'product_quantity': 2})
        response_add_2 = self.client.post(url_add,
                                          {'action': 'post', 'product_id': self.product2.id, 'product_quantity': 1})
        assert response_add_1.status_code == 200
        assert response_add_2.status_code == 200

        # Delete one product from the cart
        url_delete = reverse('cart_delete')
        response_delete = self.client.post(url_delete, {'action': 'post', 'product_id': self.product1.id})
        assert response_delete.status_code == 200

        # Verify the cart content after deletion
        cart_summary_url = reverse('cart_summary')
        cart_summary_response = self.client.get(cart_summary_url)
        assert cart_summary_response.status_code == 200
        assert 'cart' in cart_summary_response.context
        cart = cart_summary_response.context['cart']

        # Check that the deleted product is no longer in the cart
        cart_products = [item['product'] for item in cart]
        assert self.product1 not in cart_products

        # Check that the other product is still in the cart with the correct quantity
        remaining_product = next(item for item in cart if item['product'] == self.product2)
        assert remaining_product['quantity'] == 1

    @pytest.mark.django_db
    def test_cart_update(self, setup):
        browser = Client()
        url = reverse('cart_update')
        response = self.client.post(url, {'action': 'post', 'product_id': self.product.id, 'product_quantity': 5})
        assert response.status_code == 200
        assert response.json()['qty'] == 5  # Assuming the cart was updated to have three of the product
