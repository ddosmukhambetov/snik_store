from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

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
        ordering = ['-id']

    def __str__(self):
        return f'ShippingAddress - {self.full_name}'

    def get_absolute_url(self):
        return reverse('payment:shipping')

    @classmethod
    def create_default_shipping_address(cls, user):
        default_shipping_address = {
            'user': user,
            'full_name': 'No Name',
            'email': 'example@example.com',
            'city': 'Fill city',
            'street_address': 'Fill address',
            'apartment_address': 'Fill apartment address',
        }
        shipping_address = cls(**default_shipping_address)
        shipping_address.save()
        return shipping_address


class Order(models.Model):
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=9, decimal_places=2)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)
    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    is_paid = models.BooleanField('Is Paid', default=False)
    discount = models.PositiveIntegerField('Discount', default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-id']
        indexes = [models.Index(fields=['created_at'])]
        constraints = [models.CheckConstraint(check=models.Q(amount__gte=0), name='amount_gte_0')]

    def __str__(self):
        return 'Order object: ' + str(self.id)

    def get_absolute_url(self):
        return reverse('payment:order_detail', kwargs={'pk': self.pk})

    def get_total_price_without_discount(self):
        return sum(item.get_price() for item in self.order_items.all())

    @property
    def get_discount(self):
        if (total_price := self.get_total_price_without_discount()) and self.discount:
            return total_price * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_price(self):
        return self.get_total_price_without_discount() - self.get_discount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='order_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField('Price', max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField('Quantity', default=1)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['-id']
        constraints = [models.CheckConstraint(check=models.Q(quantity__gte=0), name='quantity_gte_0')]

    def __str__(self):
        return 'OrderItem object: ' + str(self.id)

    def get_price(self):
        return self.price * self.quantity

    @property
    def total_price(self):
        return self.price * self.quantity

    @classmethod
    def get_total_quantity_for_product(cls, product):
        return cls.objects.filter(product=product).aggregate(total_quantity=models.Sum('quantity'))[
            'total_quantity'] or 0

    @staticmethod
    def get_average_price():
        return OrderItem.objects.aggregate(average_price=models.Avg('price'))['average_price']
