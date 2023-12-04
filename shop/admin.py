from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'slug',)
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'category', 'available', 'slug', 'updated_at', 'created_at')
    list_filter = ('available', 'category', 'updated_at', 'created_at')
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
