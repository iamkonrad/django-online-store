import pytest
from django.contrib.auth.models import User
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
        email = 'jimm21y@stg.com'
        user = User.objects.create_user(username=username, password=password,email=email, is_active=True)

        shipping_address = ShippingAddress.objects.create(
            user=user,
            full_name='Jimmy Wang',
            email='jimm21y@stg.com',
            address1='13 Main St',
            address2='Apt 4B',
            city='Somethingtown',
            postal_code='12345',
            state='Alaska',
        )

        yield user, shipping_address, password
        shipping_address.delete()
        user.delete()


@pytest.fixture
def auth_user_without_shipping():
    with transaction.atomic():
        username = 'randomuser12'
        password = 'LT3@#yyuve'
        email = 'johnny@stg.com'
        user = User.objects.create_user(username=username, password=password, email=email, is_active=True)
        yield user, password
        user.delete()

@pytest.fixture
def unauth_user():
    with transaction.atomic():
        username = 'randomuser132'
        password = 'LwMNyhe#yyuve'
        email ='johhny32wonka@stg.com'
        user = User.objects.create_user(username=username, password=password,is_active=False)
        yield user,password
        user.delete()



@pytest.fixture
def order(auth_user_with_shipping):
    user, shipping_address, _ = auth_user_with_shipping
    order_obj = Order.objects.create(
        full_name=shipping_address.full_name,                                                                           # Full_name from shipping_address
        email=shipping_address.email,                                                                                   # Email from shipping_address
        shipping_address=shipping_address.address1,
        amount_paid=875,
        user=user,
    )
    return order_obj


@pytest.fixture
def order_without_shipping(auth_user_without_shipping):
    user, password = auth_user_without_shipping
    order_obj = Order.objects.create(
        full_name="Jack Sparrow",
        email="jacksparrow@something.com",
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
