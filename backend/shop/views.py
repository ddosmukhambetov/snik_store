from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .models import Category, ProductProxy


# def products_view(request):
#     products = ProductProxy.objects.all()
#     return render(request, 'shop/products.html', {'products': products})

class ProductsView(ListView):
    model = ProductProxy
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 15


def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy.objects.select_related('category'), slug=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if product.reviews.filter(created_by=request.user).exists():
                messages.error(request, 'You have already reviewed this product')
            else:
                rating = request.POST.get('rating', 5)
                content = request.POST.get('content', '')
                if content:
                    product.reviews.create(created_by=request.user, product=product, rating=rating, content=content)
                    return redirect(request.path)
        else:
            messages.error(request, 'You must be logged in to review')
    return render(request, 'shop/product_detail.html', {'product': product})


def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products
    })


def search_products_view(request):
    query = request.GET.get('search_query')
    products = ProductProxy.objects.filter(title__icontains=query).distinct()
    if not query or not products:
        return redirect('products')
    return render(request, 'shop/products.html', {'products': products})
