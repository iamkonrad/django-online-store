import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory, Client
from django.db import transaction

from store.models import Product
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.shortcuts import render
from payment.views import checkout, complete_order, payment_success, payment_failed

@pytest.fixture
def client():
    return RequestFactory()

@pytest.fixture
def authenticated_user():
    with transaction.atomic():
        user = User.objects.create_user(username='testuser', password='testpassword')
        yield user
        user.delete()

@pytest.fixture
def non_authenticated_user():
    return User(username='non_authenticated_user')

@pytest.mark.django_db
def test_checkout_authenticated_user_with_shipping_address(client, authenticated_user):
    request = client.get(reverse('checkout'))
    request.user = authenticated_user
    response = checkout(request)
    assert response.status_code == 200
    assert response.template_name == 'payment/checkout.html'
    assert 'shipping' in response.context

#@pytest.mark.django_db
#def test_checkout_authenticated_user_with_shipping_address(client):
    user = User.objects.get(username='testuser', password='testpassword')

    c = Client()
    c.force_login(user)

    response = c.get(reverse('checkout'))

    assert response.status_code == 200
    assert response.template_name == 'payment/checkout.html'
    assert 'shipping' in response.context

@pytest.mark.django_db
def test_checkout_authenticated_user_without_shipping_address(client, authenticated_user):
    request = client.get(reverse('checkout'))
    request.user = authenticated_user
    ShippingAddress.objects.filter(user=authenticated_user).delete()
    response = checkout(request)
    assert response.status_code == 200
    assert response.template_name == 'payment/checkout.html'
    assert 'shipping' not in response.context


@pytest.mark.django_db
def test_checkout_guest_user(client):
    request = client.get(reverse('checkout'))
    response = checkout(request)
    assert response.status_code == 200
    assert response.template_name == 'payment/checkout.html'
    assert 'shipping' not in response.context
@pytest.mark.django_db
def test_checkout_non_authenticated_user(client, non_authenticated_user):
    request = client.get(reverse('checkout'))
    request.user = non_authenticated_user
    response = checkout(request)
    assert response.status_code == 302
    assert 'login' in response.url

@pytest.mark.django_db
def test_complete_order_authenticated_user(client, authenticated_user):
    request = client.post(reverse('complete_order'), {
        'action': 'post',
        'name': 'Test User',
        'email': 'testuser@example.com',
        'address1': 'Test Address 1',
        'address2': 'Test Address 2',
        'city': 'Test City',
        'state': 'Test State',
        'postal_code': '12345',
    })
    request.user = authenticated_user
    cart = Cart(request)
    product = Product.objects.create(name="Test Product", price=100)
    cart.add(product=product, product_qty=3)  # Use cart.add with product and product_qty
    response = complete_order(request)
    assert response.status_code == 200
    assert response.json()['success'] == True

@pytest.mark.django_db
def test_complete_order_guest_user(client):
    request = client.post(reverse('complete_order'), {
        'action': 'post',
        'name': 'Test User',
        'email': 'testuser@example.com',
        'address1': 'Test Address 1',
        'address2': 'Test Address 2',
        'city': 'Test City',
        'state': 'Test State',
        'postal_code': '12345',
    })
    cart = Cart(request)
    product = Product.objects.create(name="Test Product", price=100)
    cart.add(product=product, product_qty=3)  # Use cart.add with product and product_qty
    response = complete_order(request)
    assert response.status_code == 200
    assert response.json()['success'] == True


@pytest.mark.django_db
def test_payment_success_authenticated_user(client,authenticated_user):
    request = client.get(reverse('payment_success'))
    response = payment_success(request)
    assert response.status_code == 200
@pytest.mark.django_db
def test_payment_success_guest_user(client):
    request = client.get(reverse('payment_success'))
    response = payment_success(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_failed_authenticated_user(client,authenticated_user):
    request = client.get(reverse('payment_failed'))
    response = payment_failed(request)
    assert response.status_code == 200
@pytest.mark.django_db
def test_payment_failed_guest_user(client):
    request = client.get(reverse('payment_failed'))
    response = payment_failed(request)
    assert response.status_code == 200

