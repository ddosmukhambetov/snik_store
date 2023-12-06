from django.urls import path

from .views import category_detail_view, product_detail_view, products_view

app_name = 'shop'

urlpatterns = [
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    path('category/<slug:slug>/', category_detail_view, name='category-detail'),
]
