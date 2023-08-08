import pytest
from django.test import Client, RequestFactory
from django.urls import reverse
from .cart import Cart


@pytest.mark.django_db #OK
def test_cart_summary():
    client = Client()
    response = client.get(reverse('cart-summary'))
    assert response.status_code == 200
    assert 'cart' in response.context


@pytest.mark.django_db #OK
def test_cart_add(product):
    client = Client()
    url = reverse('cart-add')
    response = client.post(url, {'action': 'post', 'product_id': product.id, 'product_quantity': 3})
    assert response.status_code == 200
    assert response.json()['qty'] == 3

@pytest.mark.django_db #OK
def test_cart_delete(product):
    client = Client()
    add_url = reverse('cart-add')                                                                                       #Add product to the cart
    response = client.post(add_url, {'action': 'post', 'product_id': product.id, 'product_quantity': 1})
    assert response.status_code == 200
    assert response.json()['qty'] == 1                                                                                  #Total quantity after addition


    delete_url = reverse('cart-delete')                                                                                 #Delete product from the cart
    response = client.post(delete_url, {'action': 'post', 'product_id': product.id})

    assert response.status_code == 200
    assert response.json()['qty'] == 0                                                                                  #Final quantity after deleting the product

@pytest.mark.django_db #OK
def test_cart_delete_non_existent_product(product):
    client = Client()
    delete_url = reverse('cart-delete')
    response = client.post(delete_url, {'action': 'post', 'product_id': product.id})

    if response.status_code == 200:                                                                                     #Check if the product was in the cart before deletion
        assert response.json()['qty'] == 0
    else:
        assert response.status_code == 404                                                                              #If there was not product in the cart throw 404

@pytest.mark.django_db  #OK
def test_cart_update(product):
    client = Client()
    add_url = reverse('cart-add')
    client.post(add_url, {'action': 'post', 'product_id': product.id, 'product_quantity': 1})                           #Adding product to the cart

    update_url = reverse('cart-update')                                                                                 #Updating the cart
    response = client.post(update_url, {'action': 'post', 'product_id': product.id, 'product_quantity': 5})

    assert response.status_code == 200
    assert response.json()['qty'] == 5                                                                                  #Updated quantity is 5=it works




@pytest.mark.django_db #OK
def test_cart_contents_after_login(product, auth_user_with_shipping):
    client = Client()
    request_factory = RequestFactory()                                                                                  #needed to create a request object
    request = request_factory.get(reverse('cart-summary'))                                                              #creating a mock request object
    request.session = client.session

    cart = Cart(request=request)                                                                                        #creating an instance of the cart class, adding a product
    cart.add(product=product, product_qty=3)
    request.session.save()                                                                                              #commiting the session

    user, shipping_address, password = auth_user_with_shipping                                                          #retrieving the user from the fixture
    client.force_login(user)


    response = client.get(reverse('cart-summary'))                                                                      #checking the contents of the cart after login
    assert response.status_code == 200


    response_cart = response.context['cart']                                                                            #extracting the cart from the response context


    assert len(response_cart) == cart.__len__()                                                                         #checking the number of items in the cart, ensuring
                                                                                                                        #the lengths are the same