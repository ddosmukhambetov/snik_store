from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress


@login_required(login_url='accounts:login')
def shipping_view(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ObjectDoesNotExist:
        shipping_address = None
    form = ShippingAddressForm(instance=shipping_address)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            form.save()
            return redirect('cart:cart-view')
    return render(request, 'shipping/shipping.html', {'form': form})


def checkout_view(request):
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')


def complete_order_view(request):
    if request.POST.get('action') == 'payment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        city = request.POST.get('city')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        zip_code = request.POST.get('zip_code')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': name,
                'email': email,
                'country': country,
                'city': city,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'zip_code': zip_code,
            }
        )
        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)
            for item in cart:
                OrderItem.objects.create(user=request.user, order=order, product=item['product'], price=item['price'],
                                         quantity=item['qty'])
        else:
            order = Order.objects.create(shipping_address=shipping_address, amount=total_price)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['qty'])
        return JsonResponse({'success': True})


def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail_view(request):
    return render(request, 'payment/payment_fail.html')
