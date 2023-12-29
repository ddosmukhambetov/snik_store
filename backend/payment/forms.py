from django import forms

from .models import Order, OrderItem, ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('full_name', 'email', 'country', 'city', 'street_address', 'apartment_address', 'zip_code')
        exclude = ('user',)
