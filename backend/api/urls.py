from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import (ProductDetailApiView, ProductListApiView,
                    ReviewCreateApiView)

app_name = 'api'
schema_view = get_schema_view(
    openapi.Info(
        default_version='v1',
        title='Snik STORE API',
        description='API for Snik STORE project',
        terms_of_service='https://example.com/terms/',
        contact=openapi.Contact(email='example@example.com'),
        license=openapi.License(name='Example License'),
    ),
    public=True,
)

urlpatterns = [
    path('products/', ProductListApiView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailApiView.as_view(), name='product-detail-list'),
    path('review/create/', ReviewCreateApiView.as_view(), name='review-create'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
