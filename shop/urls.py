from django.urls import path

from .views import (ProductsView, category_detail_view, product_detail_view,
                    search_products_view)

app_name = 'shop'

urlpatterns = [
    path('page/<int:page>', ProductsView.as_view(), name='paginator'),
    path('search/', search_products_view, name='search'),
    path('category/<slug:slug>/', category_detail_view, name='category-detail'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),
]
