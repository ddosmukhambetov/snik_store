from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, ProductProxy


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded_file = SimpleUploadedFile('small_img.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(title='Test Category')
        self.product = ProductProxy.objects.create(title='Test Product', category=self.category, image=uploaded_file)

    def test_status_code(self):
        response = self.client.get(reverse('shop:category-detail', kwargs={'slug': 'test-category'}))
        self.assertEqual(response.status_code, 200)

    def test_used_template(self):
        response = self.client.get(reverse('shop:category-detail', kwargs={'slug': 'test-category'}))
        self.assertTemplateUsed(response, 'shop/category_detail.html')

    def test_context_data(self):
        response = self.client.get(reverse('shop:category-detail', kwargs={'slug': 'test-category'}))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)


class ProductViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded_file = SimpleUploadedFile('small_img.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(title='Test Category 1')
        self.product_1 = Product.objects.create(title='Test Product 1', category=category, image=uploaded_file)
        self.product_2 = Product.objects.create(title='Test Product 2', category=category, image=uploaded_file)

    def test_status_code(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test_get_products(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(len(response.context['products']), 2)
        self.assertEqual(list(response.context['products']), [self.product_1, self.product_2])
        self.assertContains(response, self.product_1)
        self.assertContains(response, self.product_2)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded_file = SimpleUploadedFile('small_img.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(title='Test Category')
        self.product = Product.objects.create(title='Test Product', category=category, image=uploaded_file)

    def test_status_code(self):
        response = self.client.get(reverse('shop:product-detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test_get_product_by_slug(self):
        response = self.client.get(reverse('shop:product-detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['product'].slug, self.product.slug)
