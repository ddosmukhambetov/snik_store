from django.urls import path

from .views import cart_add_view, cart_delete_view, cart_update_view, cart_view

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart-view'),
    path('add/', cart_add_view, name='cart-add'),
    path('delete/', cart_delete_view, name='delete-from-cart'),
    path('update/', cart_update_view, name='cart-update'),
]
