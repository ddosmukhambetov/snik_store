from django.contrib.auth import get_user_model
from rest_framework import serializers

from recommendations.models import Review
from shop.models import Category, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(many=False, slug_field='title', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'brand', 'price', 'image', 'category', 'created_at', 'updated_at')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'product_id', 'rating', 'content', 'created_by', 'created_at')
        read_only_fields = ('id', 'created_by', 'created_at')


class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(many=False, slug_field='title', queryset=Category.objects.all())
    discount_price = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'brand', 'price', 'image', 'category', 'created_at', 'updated_at',
                  'discount_price', 'reviews')

    def get_discount_price(self, obj):
        discount_price = obj.get_discount_price()
        return str(discount_price)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        user = User(email=email, username=username)
        user.set_password(validated_data['password'])
        user.save()
        return user
