import pytest
from django.test import Client
from django.urls import reverse
from .models import Category, Product

@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', slug='test-category')

@pytest.fixture                                                                                                         #test product, dependant on the category "fixture"
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


