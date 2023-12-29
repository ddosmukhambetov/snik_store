from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.models import Product

User = get_user_model()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField('Content', max_length=500)
    rating = models.PositiveSmallIntegerField('Rating', validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateField('Created Date', auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f'Review created by {self.created_by} for {self.product}'
