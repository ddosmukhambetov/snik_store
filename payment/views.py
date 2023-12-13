import uuid
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from yookassa import Configuration, Payment

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


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
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return redirect('payment:shipping')


def complete_order_view(request):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')
        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        city = request.POST.get('city')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        zip_code = request.POST.get('zip_code')

        cart = Cart(request)
        total_price = cart.get_total_price()

        match payment_type:
            case 'stripe-payment':
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
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment-fail')),
                    'line_items': [],
                }
                if request.user.is_authenticated:
                    order = Order.objects.create(user=request.user, shipping_address=shipping_address,
                                                 amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(user=request.user, order=order, product=item['product'],
                                                 price=item['price'], quantity=item['qty'])
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product']
                                },
                            },
                            'quantity': item['qty'],
                        })
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)
                else:
                    order = Order.objects.create(shipping_address=shipping_address, amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                                 quantity=item['qty'])
            case 'yookassa-payment':
                idempotence_key = uuid.uuid4()
                payment = Payment.create({
                    'amount': {
                        'value': str(total_price * 90),
                        'currency': 'RUB',
                    },
                    'confirmation': {
                        'type': 'redirect',
                        'return_url': request.build_absolute_uri(reverse('payment:payment-success')),
                    },
                    'capture': True,
                    'test': True,
                    'description': 'Products in cart'
                }, idempotence_key)
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
                    order = Order.objects.create(user=request.user, shipping_address=shipping_address,
                                                 amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(user=request.user, order=order, product=item['product'],
                                                 price=item['price'], quantity=item['qty'])
                    return redirect(payment.confirmation.confirmation_url)
                else:
                    order = Order.objects.create(shipping_address=shipping_address, amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                                 quantity=item['qty'])


def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail_view(request):
    return render(request, 'payment/payment_fail.html')
