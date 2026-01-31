from django.shortcuts import get_object_or_404, render
from .models import Category, Product


# Create your views here.

# def categories(request):
#     return {
#         'categories': Category.objects.all()
#     }
#

def product_all(request):

    print(request.META['REMOTE_ADDR'])
    # products = Product.products.all()
    products = Product.products.prefetch_related("product_image").filter(is_active=True)

    # products = Product.objects.all()
    return render(request, 'store/index.html', {
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/single.html', {
        'product': product
    })


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, 'store/category.html', {
        'category': category,
        'products': products
    })


# 1:29