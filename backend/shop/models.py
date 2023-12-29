from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField('Title', max_length=255, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    created_at = models.DateTimeField('Created Date', auto_now_add=True)
    slug = models.SlugField('Slug', max_length=255, unique=True, null=False, editable=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('slug', 'parent')

    def __str__(self):
        full_path = [self.title]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.title)
            parent = parent.parent
        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category-detail', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description', blank=True)
    brand = models.CharField('Brand', max_length=255)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2, default=77.77)
    image = models.ImageField('Image', upload_to='products/products/%Y/%m/%d', default='products/default_product.webp')
    available = models.BooleanField('Available', default=True)
    created_at = models.DateTimeField('Created Date', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Updated Date', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField('Slug', max_length=255)
    discount = models.PositiveIntegerField('Discount', default=0,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.slug})

    def get_discount_price(self):
        discount_price = self.price - (self.price * self.discount / 100)
        return round(discount_price, 2)

    @property
    def full_image_url(self):
        return self.image.url if self.image else ''


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    object = ProductManager()

    class Meta:
        proxy = True
