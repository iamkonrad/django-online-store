import pytest
from django.test import Client
from django.urls import reverse
from .models import Category, Product

@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', slug='test-category')

@pytest.fixture                                                                                                         #test product, dependent on the category "fixture"
def product(category):
    return Product.objects.create(title='Test Product', slug='test-product', category=category,price=19.99, image ='images/')

@pytest.mark.django_db
def test_store():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200
    assert 'all_products' in response.context

@pytest.mark.django_db
def test_categories():
    client = Client()
    response = client.get('/')
    assert 'all_categories' in response.context

@pytest.mark.django_db
def test_list_category(category):
    client = Client()
    url = reverse('list-category', kwargs={'category_slug': category.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert 'category' in response.context

@pytest.mark.django_db
def test_product_info(product):
    client = Client()
    url = reverse('product-info', kwargs={'product_slug': product.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert 'product' in response.context



# @pytest.mark.django_db
# def test_product_creation():
#     product = Product.objects.create(title='New Product', slug='new-product', price=9.99, image='images/')
#     assert Product.objects.filter(slug='new-product').exists()
#

# @pytest.mark.django_db
# def test_category_creation():
#     category = Category.objects.create(name='New Category', slug='new-category')
#     assert Category.objects.filter(slug='new-category').exists()
#



# @pytest.mark.django_db
# def test_product_deletion(product):
#     product.delete()
#     assert not Product.objects.filter(slug=product.slug).exists()
#

# @pytest.mark.django_db
# def test_category_deletion(category):
#     category.delete()
#     assert not Category.objects.filter(slug=category.slug).exists()
#
# @pytest.mark.django_db
# def test_add_product_to_category(category, product):
#     category.products.add(product)
#     assert product in category.products.all()
#
# @pytest.mark.django_db
# def test_remove_product_from_category(category, product):
#     category.products.add(product)
#     category.products.remove(product)
#     assert product not in category.products.all()
#
# @pytest.mark.django_db
# def test_product_price_change(product):
#     new_price = 29.99
#     product.price = new_price
#     product.save()
#     updated_product = Product.objects.get(slug=product.slug)
#     assert updated_product.price == new_price