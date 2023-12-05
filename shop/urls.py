from django.urls import path, include
from .views import products_view, product_detail_view, category_detail_view

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    path('category/<slug:slug>/', category_detail_view, name='category-detail'),
]
