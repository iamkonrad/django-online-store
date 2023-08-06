import pytest
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.urls import reverse
from .models import Category, Product, Tag




@pytest.mark.django_db #OK
def test_empty_store_view(client):
    client=Client()
    Product.objects.all().delete()
    url = reverse('store')
    response = client.get(url)
    assert response.status_code == 200
    assert 'all_products' in response.context
    assert len(response.context['all_products']) == 0


@pytest.mark.django_db #OK
def test_random_category_creation():
    client = Client()
    category = Category.objects.create(name='Lingerie', slug='lingerie')

    assert Category.objects.filter(slug='lingerie').exists()

    url = reverse('list-category', args=[category.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert category.name == 'Lingerie'
    assert category.slug == 'lingerie'


@pytest.mark.django_db #OK
def test_random_category_deletion():
    category = Category.objects.create(name='Random Category', slug='random-category')
    assert Category.objects.filter(slug='random-category').exists()
    category.delete()

    assert not Category.objects.filter(slug='random-category').exists()


@pytest.mark.django_db #OK
def test_add_product_to_existing_category():
    product = Product.objects.create(title='Winter gloves', price=50.00)
    category = Category.objects.create(name='shirts', slug='shirts')
    product.category = category
    product.save()

    assert product in category.product.all()



@pytest.mark.django_db#
def test_existing_category_on_homepage():
    client = Client()
    category_slug = 'shirts'
    category = Category.objects.create(slug=category_slug)
    url = reverse('list-category', kwargs={'category_slug': category_slug})
    response = client.get(url)

    assert response.status_code == 200
    assert 'category' in response.context


@pytest.mark.django_db #OK
def test_non_existing_category_on_homepage():
    client = Client()
    non_existing_categories = ['Socks']

    for category_slug in non_existing_categories:
        with pytest.raises(ObjectDoesNotExist):
            Category.objects.get(slug=category_slug)

        url = reverse('list-category', kwargs={'category_slug': category_slug})
        response = client.get(url)

        assert response.status_code == 404

@pytest.mark.django_db
def test_existing_product_slug():
    client = Client()
    product_slug = 'female-hat'
    product_price = 18.00
    image = 'images/'
    product = Product.objects.create(slug=product_slug, price=product_price, image=image)
    url = reverse('product-info', kwargs={'product_slug': product.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert 'product' in response.context

@pytest.mark.django_db #OK
def test_non_existing_product_slug():
    client = Client()
    product_slug = 'cat-toy'

    with pytest.raises(ObjectDoesNotExist):                                                                             #exception is raised since it doesn't exist
        Product.objects.get(slug=product_slug)

    url = reverse('product-info', kwargs={'product_slug': product_slug})
    response = client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db #OK
def test_product_creation():
    product = Product.objects.create(title='popeye pants', slug='popeye pants', price=9.99, image='images/')
    assert Product.objects.filter(slug='popeye pants').exists()



#################################
@pytest.mark.django_db #OK
def test_product_price_change():
    product = Product.objects.create(title="Female Hat", price=150.00)
    new_price = Decimal('29.99')
    product.price = new_price
    product.save()

    updated_product = Product.objects.get(slug=product.slug)
    assert updated_product.price == new_price

@pytest.mark.django_db #OK
def test_search_view_non_existing_product():
    client = Client()
    search_query = 'The Sorting Hat'
    response = client.get('/search/', {'search_query': search_query})
    assert response.status_code == 200
    assert 'results' in response.context
    assert 'query' in response.context
    assert not response.context['results']

@pytest.mark.django_db #OK
def test_search_view_existing_product():
    client = Client()
    search_query = 'Female Hat'
    response = client.get('/search/', {'search_query': search_query})
    assert response.status_code == 200
    assert 'results' in response.context
    assert 'query' in response.context
    assert not response.context['results']

@pytest.mark.django_db #OK
def test_tag_unique_name():
    Tag.objects.create(tag_name='Best Sellers')
    with pytest.raises(Exception):
        Tag.objects.create(tag_name='Best sellers')
@pytest.mark.django_db #OK
def test_tag_unique_slug():
    Tag.objects.create(tag_name='Best Sellers', tag_slug='best-sellers')
    with pytest.raises(Exception):
        Tag.objects.create(tag_name='New Arrivals', tag_slug='best-sellers')

@pytest.mark.django_db #OK
def test_tag_absolute_url():
    tag = Tag.objects.create(tag_name='Best Sellers', tag_slug='best-sellers')
    url = reverse('list-tag', args=[tag.tag_slug])
    assert url == f'/tag/{tag.tag_slug}/'                                                                               #checking whether appropriate tag slug URL will be constructed

@pytest.mark.django_db #OK
def test_tag_creation():
    tag = Tag.objects.create(tag_name='Best Sellers', tag_slug='best-sellers')
    assert isinstance(tag, Tag)
    assert str(tag) == 'Best Sellers'

@pytest.mark.django_db #OK
def test_tag_deletion():
    tag = Tag.objects.create(tag_name='Summer bestseller', tag_slug='summer-bestseller')
    tag_count_before = Tag.objects.count()

    tag.delete()
    tag_count_after = Tag.objects.count()

    assert tag_count_after == tag_count_before - 1
