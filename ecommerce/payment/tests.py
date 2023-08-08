import json

import pytest
from django.urls import reverse
from django.test import RequestFactory, Client

from .models import Order, OrderItem, Product
from cart.cart import Cart
from payment.views import complete_order, payment_success, payment_failed



@pytest.mark.django_db #OK
def test_checkout_auth_user_with_shipping_address(auth_user_with_shipping):
    client = Client()
    user, shipping_address, password = auth_user_with_shipping
    client.force_login(user)
    response = client.get(reverse('checkout'))

    assert response.status_code == 200
    assert 'payment/checkout.html' in [template.name for template in response.templates]
    assert response.context['shipping'] == shipping_address



@pytest.mark.django_db #OK
def test_checkout_auth_user_without_shipping_address(auth_user_without_shipping):
    client = Client()
    user, password = auth_user_without_shipping
    client.force_login(user)
    response = client.get(reverse('checkout'))
    assert response.status_code == 200

    data = {
        'name': user.username,                                                                                          #Using the username as the name
        'email': user.email,                                                                                            # Using the email from the fixture
    }
    response = client.post(reverse('checkout'), data=data)
    assert response.status_code == 200

@pytest.mark.django_db #OK
def test_checkout_guest_user():
    client = Client()
    response = client.get(reverse('checkout'))

    assert response.status_code == 200
    assert 'payment/checkout.html' in response.templates[0].name                                                        #checks whether 1st template used is checkout
    assert 'shipping' not in response.context                                                                           #guest_user has no shipping info saved


@pytest.mark.django_db #OK
def test_complete_order_auth_user_with_shipping(auth_user_with_shipping, product):
    client = Client()
    user, shipping_address,password = auth_user_with_shipping
    client.force_login(user)

    request_factory = RequestFactory()                                                                                  #Need to create a fake request to make sure that the request
    request = request_factory.get('/')                                                                                  #object is passed to the cart constructor
    request.session = client.session

    cart = Cart(request)                                                                                                #cart utilising the fake request
    cart.add(product=product, product_qty=3)

    request.session['session_key'] = cart.cart                                                                          #session updated with the modified cart
    request.session.save()

    response = client.post(reverse('complete_order'), {                                                                 #post request simulated to the complete_order view
        'action': 'post',
        'name': 'Test User',
        'email': 'testuser@example.com',
        'address1': 'Test Address 1',
        'address2': 'Test Address 2',
        'city': 'Test City',
        'state': 'Test State',
        'postal_code': '12345',
    })

    assert response.status_code == 200
    assert response.json()['success'] == True

@pytest.mark.django_db #OK
def test_complete_order_guest_user():
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
    product = Product.objects.create(title="Test Product", price=100)
    cart.add(product=product, product_qty=3)                                                                            # Cart.add with product and product_qty
    response = complete_order(request)
    assert response.status_code == 200
    response_content = json.loads(response.content)                                                                     #JSON needed because of the JS
    assert response_content['success'] == True

@pytest.mark.django_db #OK
def test_payment_success_auth_user_with_shipping(auth_user_with_shipping):
    client = Client()
    user = auth_user_with_shipping[0]                                                                                   # The user object is the first item in the list
    client.force_login(user)                                                                                            # Force login the authenticated user

    response = client.get(reverse('payment-success'))                                                                    # A request to the 'payment-success' URL
    response = payment_success(response.wsgi_request)                                                                    # The view function
    assert response.status_code == 200


@pytest.mark.django_db #OK
def test_payment_success_auth_user_without_shipping(auth_user_without_shipping):
    client=Client()
    user, password=auth_user_without_shipping
    client.force_login(user)
    response = client.get(reverse('payment-success'))
    assert response.status_code == 200

@pytest.mark.django_db #OK
def test_payment_success_guest_user():
    client = Client()
    response = client.get(reverse('payment-success'))
    assert response.status_code == 200

@pytest.mark.django_db #OK
def test_payment_failed_auth_user_with_shipping(auth_user_with_shipping):
    client = Client()
    user = auth_user_with_shipping[0]                                                                                   # The user object is the first item in the list
    client.force_login(user)                                                                                            # Force login the authenticated user

    response = client.get(reverse('payment-failed'))                                                                    # A request to the 'payment-failed' URL
    response = payment_failed(response.wsgi_request)                                                                    # The view function
    assert response.status_code == 200

@pytest.mark.django_db #OK
def test_payment_failed_authenticated_user_without_shipping(auth_user_without_shipping):                                #Yielding only the user, no need to access
    client = Client()                                                                                                   #The list
    user, password=auth_user_without_shipping
    client.force_login(user)                                                                                            # Force login the authenticated user

    response = client.get(reverse('payment-failed'))                                                                    # A request to the 'payment-failed' URL
    response = payment_failed(response.wsgi_request)                                                                    # The view function
    assert response.status_code == 200

@pytest.mark.django_db #OK
def test_payment_failed_guest_user():
    client=Client()
    response = client.get(reverse('payment-failed'))
    assert response.status_code == 200


@pytest.mark.django_db #OK
def test_order_total_amount_paid(order, order_item_1, order_item_2):
    assert order.amount_paid == (order_item_1.quantity * order_item_1.price) + (order_item_2.quantity * order_item_2.price)



@pytest.mark.django_db
def test_order_deletion_auth_user_with_shipping(auth_user_with_shipping, product, order, order_item_1):
    client = Client()
    user, shipping_address, password = auth_user_with_shipping
    login = client.login(username=user.username, password=password)
    assert login is True

    assert user.username == 'randomuser'
    assert shipping_address.address1 == '13 Main St'

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1

    order.delete()

    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0

@pytest.mark.django_db #OK
def test_order_deletion_auth_user_without_shipping(auth_user_without_shipping, product, order, order_item_1):
    client = Client()
    user, password = auth_user_without_shipping
    login = client.login(username=user.username, password=password)
    assert login is True

    assert user.username == 'randomuser12'

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1

    order.delete()

    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0

@pytest.mark.django_db #OK
def test_order_deletion_guest_user(product,order, order_item_1):

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1

    order.delete()

    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0
