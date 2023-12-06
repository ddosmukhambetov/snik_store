from django.shortcuts import get_object_or_404, render

from .models import Category, ProductProxy


def products_view(request):
    products = ProductProxy.objects.all()
    return render(request, 'shop/products.html', {'products': products})


def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products
    })
