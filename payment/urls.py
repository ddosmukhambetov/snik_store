from django.urls import path

from .views import (checkout_view, complete_order_view, payment_fail_view,
                    payment_success_view, shipping_view)

app_name = 'payment'

urlpatterns = [
    path('shipping/', shipping_view, name='shipping'),
    path('checkout/', checkout_view, name='checkout'),
    path('complete-order/', complete_order_view, name='complete-order'),
    path('payment-success/', payment_success_view, name='payment-success'),
    path('payment-fail/', payment_fail_view, name='payment-fail'),
]
