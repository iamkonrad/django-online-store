import pytest

from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from payment.models import ShippingAddress


@pytest.mark.django_db #OK
def test_new_user_registration():
    client=Client()
    url = reverse('register')
    data = {
        'username': 'testuse12',
        'email': 'someemail@email.com',
        'password1': 'YTHd2145Ds',
        'password2': 'YTHd2145Ds'
    }
    response = client.post(url, data)
    assert response.status_code == 302                                                                                  #successful registration
    assert response.url == reverse('email-verification-sent')
    assert User.objects.filter(email='someemail@email.com').exists()

@pytest.mark.django_db #OK
def test_user_without_shipping_login(auth_user_without_shipping):
    client = Client()
    user,password = auth_user_without_shipping
    url = reverse('my-login')
    response = client.post(url, {'username': user.username, 'password': password})
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert auth.get_user(client).is_authenticated

@pytest.mark.django_db #OK
def test_user_with_shipping_login(auth_user_with_shipping):
    client = Client()
    user, shipping_address, password = auth_user_with_shipping
    url = reverse('my-login')
    response = client.post(url, {'username': user.username, 'password': password})

    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert auth.get_user(client).is_authenticated


@pytest.mark.django_db #OK
def test_inactive_user_login(unauth_user):
    client = Client()
    user = unauth_user
    url = reverse('my-login')
    response = client.post(url, {'username': user.username})

    assert response.status_code == 200                                                                                  #the request was processed successfully, but
    assert not auth.get_user(client).is_authenticated                                                                   #the user is not authenticated, so he won't be
                                                                                                                        #allowed to login
@pytest.mark.django_db
def test_inactive_user_login(unauth_user):
    client = Client()
    user,password = unauth_user
    url = reverse('my-login')
    response = client.post(url, {'username': user.username, 'password': password})

    assert response.status_code != 302                                                                                  #asserts status code is different from 302, that is
    assert not auth.get_user(client).is_authenticated                                                                   #a successful login

@pytest.mark.django_db #OK
def test_user_without_shipping_logout(auth_user_without_shipping):
    client=Client()
    user, password = auth_user_without_shipping                                                                         # Unpack the user from the tuple
    client.force_login(user)                                                                                            # Pass the user object
    url = reverse('user-logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('store')
    assert not auth.get_user(client).is_authenticated

@pytest.mark.django_db #OK
def test_user_with_shipping_logout(auth_user_with_shipping):
    client=Client()
    user, shipping_address,password = auth_user_with_shipping
    client.force_login(user)
    url = reverse('user-logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('store')
    assert not auth.get_user(client).is_authenticated

@pytest.mark.django_db #OK
def test_profile_management_user_with_shipping(auth_user_with_shipping):
    client=Client()
    user, shipping_address, password = auth_user_with_shipping
    client.force_login(user)
    url = reverse('profile-management')
    data = {'username': user.username, 'email': user.email}
    response = client.post(url, data)
    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert user.username == user.username
    assert user.email == user.email

@pytest.mark.django_db #OK
def test_profile_management_user_without_shipping(auth_user_without_shipping):
    client=Client()
    user, password=auth_user_without_shipping
    client.force_login(user)
    url = reverse('profile-management')
    data = {'username': user.username, 'email': user.email}
    response = client.post(url, data)
    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert user.username == user.username
    assert user.email == user.email

@pytest.mark.django_db #OK
def test_delete_account_user_with_shipping(auth_user_with_shipping):
    client = Client()
    user, shipping_address, password = auth_user_with_shipping
    client.force_login(user)

    url = reverse('delete-account')
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('store')

    with pytest.raises(User.DoesNotExist):
        user.refresh_from_db()


@pytest.mark.django_db  # OK
def test_delete_account_user_without_shipping(auth_user_without_shipping):
    client = Client()
    user, password = auth_user_without_shipping
    client.force_login(user)

    url = reverse('delete-account')
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('store')

    with pytest.raises(User.DoesNotExist):
        user.refresh_from_db()

@pytest.mark.django_db
def test_manage_shipping_user_with_shipping(auth_user_with_shipping):
    client = Client()
    user, shipping_address, password = auth_user_with_shipping
    client.force_login(user)
    url = reverse('manage-shipping')

    response_get = client.get(url)                                                                                      #the GET request to check if the form is pre-filled
    form = response_get.context['form']
    assert form.initial['full_name'] == 'Jimmy Wang'

    response_post = client.post(url, {                                                                                  #Simulate submitting the form with get
        'full_name': 'Jimmy Wang',
        'email': 'jimm21y@stg.com',
        'address1': '13 Main St',
        'address2': 'Apt 4B',
        'city': 'Somethingtown',
        'postal_code': '12345',
        'state': 'Alaska',
    })

    assert response_post.status_code == 302                                                                             #302 redirects to the dashboard as expected
    dashboard_url = reverse('dashboard')
    assert response_post.url == dashboard_url


@pytest.mark.django_db
def test_manage_shipping_user_without_shipping(auth_user_without_shipping):
    client = Client()
    user, password = auth_user_without_shipping
    client.force_login(user)
    url = reverse('manage-shipping')

    response_get = client.get(url)
    assert response_get.status_code == 200                                                                              #The form is rendering correctly

    data = {
        'full_name': 'Jimmy Chow',
        'email': 'john@something.com',
        'address1': '123 Main St',
        'address2': 'Apt 2G',
        'city': 'New York',
        'postal_code': '10031',
        'state': 'NY',
    }
    response_post = client.post(url, data=data)
    assert response_post.status_code == 302
    assert response_post.url == reverse('dashboard')                                                                    #Redirect after submission to dashboard

    shipping_address = ShippingAddress.objects.get(user=user)                                                           #Form saved in the database
    assert shipping_address.full_name == 'Jimmy Chow'
    assert shipping_address.email == 'john@something.com'
    assert shipping_address.address1 == '123 Main St'
    assert shipping_address.address2 == 'Apt 2G'
    assert shipping_address.city == 'New York'
    assert shipping_address.postal_code == '10031'
    assert shipping_address.state == 'NY'

@pytest.mark.django_db
def test_track_orders_user_with_shipping(auth_user_with_shipping, order):
    client = Client()
    user, shipping_address, password = auth_user_with_shipping
    client.force_login(user)

    url = reverse('track-orders')
    response = client.get(url)
    assert response.status_code == 200
    assert order.user == user

@pytest.mark.django_db #OK
def test_track_orders_user_without_shipping(order_without_shipping):
    client = Client()
    user = order_without_shipping.user
    client.force_login(user)

    url = reverse('track-orders')
    response = client.get(url)
    assert response.status_code == 200

    assert order_without_shipping.user == user                                                                          # Assert that the user without a
    assert 'orders' in response.context                                                                                 # shipping address has no order history
    assert len(response.context['orders']) == 0
