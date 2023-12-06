from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import ProductProxy
from django.http import JsonResponse


def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart_list.html', {'cart': cart})


def cart_add_view(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(ProductProxy, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()
        return JsonResponse({'qty': cart_qty, 'product': product.title})


def cart_delete_view(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        return JsonResponse({'qty': cart_qty, 'total': cart_total})


def cart_update_view(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        return JsonResponse({'qty': cart_qty, 'total': cart_total})
