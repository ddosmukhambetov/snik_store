from django.contrib.auth import get_user_model
from django.db import models

from shop.models import Product

User = get_user_model()


class ShippingAddress(models.Model):
    full_name = models.CharField('Full Name', max_length=255)
    email = models.EmailField('Email Address', max_length=255)
    country = models.CharField('Country', max_length=150, blank=True, null=True)
    city = models.CharField('City', max_length=150, blank=True, null=True)
    street_address = models.CharField('Street Address', max_length=150)
    apartment_address = models.CharField('Apartment Address', max_length=150)
    zip_code = models.CharField('ZIP Code', max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return 'ShippingAddress object: ' + str(self.id)


class Order(models.Model):
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=9, decimal_places=2)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)
    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    is_paid = models.BooleanField('Is Paid', default=False)

    def __str__(self):
        return 'Order object: ' + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField('Price', max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField('Quantity', default=1)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return 'OrderItem object: ' + str(self.id)
