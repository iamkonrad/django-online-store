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
def non_authenticated_user():
    return User(username='non_authenticated_user')

@pytest.fixture
def authenticated_user():
    with transaction.atomic():
        username = 'randomuser'
        password = 'LKSJYTBBVT3@#qsxyyuve'
        user = User.objects.create_user(username=username, password=password)
        yield user
        user.delete()

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


@pytest.mark.django_db #OK
def test_checkout_guest_user():
    client = Client()
    response = client.get(reverse('checkout'))

    assert response.status_code == 200
    assert 'payment/checkout.html' in response.templates[0].name                                                        #checks whether 1st template used is checkout
    assert 'shipping' not in response.context                                                                           #guest_user has no shipping info saved

@pytest.mark.django_db
def test_checkout_non_authenticated_user(non_authenticated_user):
    client=Client()
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
def test_complete_order_guest_user(authenticated_user):
    client = Client()
    response = client.post(reverse('complete_order'), {
        'action': 'post',
        'name': 'Test User',
        'email': 'testuser@example.com',
        'address1': 'Test Address 1',
        'address2': 'Test Address 2',
        'city': 'Test City',
        'state': 'Test State',
        'postal_code': '12345',
    })
    request = response.wsgi_request
    cart = Cart(request)
    product = Product.objects.create(name="Test Product", price=100)
    cart.add(product=product, product_qty=3)  # Use cart.add with product and product_qty
    response = complete_order(request)
    assert response.status_code == 200
    assert response.json()['success'] == True

@pytest.mark.django_db #OK
def test_payment_success_authenticated_user(authenticated_user):
    client=Client()
    client.force_login(authenticated_user)
    response = client.get(reverse('payment-success'))
    assert response.status_code == 200

@pytest.mark.django_db#OK
def test_payment_success_guest_user():
    client = Client()
    response = client.get(reverse('payment-success'))
    assert response.status_code == 200


@pytest.mark.django_db #OK
def test_payment_failed_authenticated_user(authenticated_user):
    # Log in the authenticated_user
    client = Client()
    logged_in = client.login(username=authenticated_user.username, password='LKSJYTBBVT3@#qsxyyuve')
    assert logged_in == True  # Verify that login was successful

    # Making a request to the 'payment-failed' URL
    response = client.get(reverse('payment-failed'))

    # Calling the view function
    response = payment_failed(response.wsgi_request)

    # Checking the status code
    assert response.status_code == 200


@pytest.mark.django_db #OK
def test_payment_failed_guest_user():
    client=Client()
    response = client.get(reverse('payment-failed'))
    assert response.status_code == 200

