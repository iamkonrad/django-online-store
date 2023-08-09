from django.shortcuts import render
from . models import Category, Product, Tag
from django.shortcuts import get_object_or_404


def store(request):
    all_products = Product.objects.all()                                                                                #getting hold of all the products
    all_tags = Tag.objects.all()                                                                                        #retrieving objects from the database

    context = {
        'all_products': all_products,
        'all_tags': all_tags,
    }

    return render(request, 'store/store.html', context)                                                                 # displayed on the store page after retrieval


def categories(request):

    all_categories=Category.objects.all()                                                                               #select all categories(shoes and shirts)

    return {'all_categories': all_categories}

def list_category(request,category_slug=None ):                                                                         #(a view for individual category)

    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(category=category)                                                            #defining the products and filtering them by category

    return render(request, 'store/list-category.html', {'category':category,'products':products})

def product_info(request,product_slug):

    product = get_object_or_404(Product,slug=product_slug)                                        #getting hold of a specific product from a database,
                                                                                                  #if it doesn't exist return an error, match the product with
    context = {'product':product}                                                                 #a slug ID, that is equal to a slug ID we are looking for

    return render(request,'store/product-info.html',context)


def search(request):
    query = request.GET.get('search_query')
    if query:
        results = Product.objects.filter(title__icontains=query)
        if not results:
            if query.endswith('s'):
                results = Product.objects.filter(title__icontains=query[:-1])
            elif query.endswith('es'):
                results = Product.objects.filter(title__icontains=query[:-2])
            elif query.endswith('ies'):
                singular_query = query[:-3] + 'y'                                                                       #berry, berries
                results = Product.objects.filter(title__icontains=singular_query)
            else:
                results = Product.objects.filter(title__icontains=query + 's')
    else:
        results = Product.objects.none()
    return render(request, 'store/search_results.html', {'results': results, 'query': query})


def list_tag(request, tag_slug=None):
    tag = get_object_or_404(Tag, tag_slug=tag_slug)
    products = tag.product_tags.all()
    all_categories = Category.objects.all()
    all_tags = Tag.objects.all()

    context = {
        'tag': tag,
        'products': products,
        'all_categories': all_categories,
        'all_tags': all_tags,
    }

    return render(request, 'store/list-tag.html', context)
