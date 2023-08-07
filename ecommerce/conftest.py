import pytest
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from payment.models import ShippingAddress, OrderItem, Order
from store.models import Category, Product, Tag

#STORE.TESTS
@pytest.fixture
def category():
    return Category.objects.create(name='Shirts', slug='shirts')

@pytest.fixture
def product(category):
    image = 'images/'
    return Product.objects.create(title='Havana shirt',slug='havana-shirt', price=50.00, category=category, image=image)

@pytest.fixture
def tag():
    return Tag.objects.create(tag_name='Best Occasions', tag_slug='best-occasions')



#PAYMENT.TESTS
@pytest.fixture
def auth_user_with_shipping():
    with transaction.atomic():
        username = 'randomuser'
        password = 'LKSJYTBBVT3@#qsxyyuve'
        user = User.objects.create_user(username=username, password=password)

        shipping_address = ShippingAddress.objects.create(
            user=user,
            full_name='John Doe',
            email='johndoe@example.com',
            address1='123 Main St',
            address2='Apt 4B',
            city='Springfield',
            postal_code='12345',
        )

        yield [user, shipping_address]
        user.delete()
        shipping_address.delete()

@pytest.fixture
def auth_user_without_shipping():
    with transaction.atomic():
        username = 'randomuser12'
        password = 'LT3@#yyuve'
        user = User.objects.create_user(username=username, password=password)
        yield user
        user.delete()

@pytest.fixture
def order(auth_user_with_shipping):
    user, shipping_address = auth_user_with_shipping
    order_obj = Order.objects.create(
        full_name="Simon Adebisi",
        email="john@something.com",
        shipping_address=shipping_address.address1,
        amount_paid=875,
        user=user,
    )
    return order_obj

@pytest.fixture
def order_item_1(order, product):
    order_item_obj = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=3,
        price=125,
    )
    return order_item_obj

@pytest.fixture
def order_item_2(order, product):
    order_item_obj = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=5,
        price=100,
    )
    return order_item_obj
