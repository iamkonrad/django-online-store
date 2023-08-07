import pytest

from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from account.token import user_tokenizer_generate, UserVerificationTokenGenerator
from django.utils.encoding import force_bytes



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



