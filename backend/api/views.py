from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions

from recommendations.models import Review
from shop.models import Category, Product

from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (ProductDetailSerializer, ProductSerializer,
                          ReviewSerializer)


class ProductListApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').order_by('pk')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardResultsSetPagination


class ProductDetailApiView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class ReviewCreateApiView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        existing_review = Review.objects.filter(product=product, created_by=self.request.user).exists()
        if existing_review:
            raise ValidationError('You have already reviewed this product.')
        serializer.save(product=product, created_by=self.request.user)
