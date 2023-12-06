import json

from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from shop.views import Category, ProductProxy
from .views import cart_view, cart_add_view, cart_delete_view, cart_update_view


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart-view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart-view')), 'cart/cart_list.html')


class CartAddViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')
        self.product = ProductProxy.objects.create(title='Test Product', category=self.category, price=10.00)
        self.factory = RequestFactory().post(reverse('cart:cart-add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 1,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add_view(self):
        request = self.factory
        response = cart_add_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 1)
        self.assertEqual(data['product'], 'Test Product')


class CartDeleteViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')
        self.product = ProductProxy.objects.create(title='Test Product', category=self.category, price=10.00)
        self.factory = RequestFactory().post(reverse('cart:delete-from-cart'), {
            'action': 'post',
            'product_id': self.product.id,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_delete_view(self):
        request = self.factory
        response = cart_delete_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 0)
        self.assertEqual(data['total'], 0)


class CartUpdateViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')
        self.product = ProductProxy.objects.create(title='Test Product', category=self.category, price=10.00)
        self.factory = RequestFactory().post(reverse('cart:cart-add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 100,
        })
        self.factory = RequestFactory().post(reverse('cart:cart-update'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 1,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_update_view(self):
        request = self.factory
        response = cart_add_view(request)
        response = cart_update_view(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 1)
        self.assertEqual(data['total'], '10.00')
