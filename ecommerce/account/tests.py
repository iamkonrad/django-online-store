import pytest

from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from account.token import user_tokenizer_generate
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

@pytest.mark.django_db
def test_email_verification_success():
    client = Client()
    user = User.objects.create(username='testuse12', email='someemail@email.com')
    user.is_active = False
    user.save()
    token = user_tokenizer_generate.make_token(user)

    # Convert the user's primary key to bytes-like object before encoding
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    url = reverse('email-verification', args=[uid, token])
    response = client.get(url)
    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('email-verification-success')
    assert user.is_active


@pytest.mark.django_db
def test_user_login(auth_user_without_shipping):
    client = Client()
    user = auth_user_without_shipping
    url = reverse('my-login')
    response = client.post(url, {'username': user.username})
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
def test_user_without_shipping_logout(auth_user_without_shipping):
    client=Client()
    client.force_login(auth_user_without_shipping)
    url = reverse('user-logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('store')
    assert not auth.get_user(client).is_authenticated

@pytest.mark.django_db #OK
def test_user_with_shipping_logout(auth_user_with_shipping):
    client=Client()
    user, shipping_address = auth_user_with_shipping
    client.force_login(user)
    url = reverse('user-logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('store')
    assert not auth.get_user(client).is_authenticated

@pytest.mark.django_db
def test_profile_management_user_without_shipping(auth_user_without_shipping):
    client=Client()
    user=auth_user_without_shipping
    client.force_login(user)
    url = reverse('profile-management')
    data = {'username': 'newuser', 'email': 'newuser@example.com'}
    response = client.post(url, data)
    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert user.username == 'newuser'
    assert user.email == 'newuser@example.com'

@pytest.mark.django_db
def test_profile_management_user_without_shipping(auth_user_without_shipping):
    client=Client()
    user = auth_user_without_shipping
    client.force_login(user)
    url = reverse('profile-management')
    data = {'username': 'newuser', 'email': 'newuser@example.com'}
    response = client.post(url, data)
    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
    assert user.username == 'newuser'
    assert user.email == 'newuser@example.com'



