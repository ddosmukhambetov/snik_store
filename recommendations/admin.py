from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'content', 'rating', 'created_by', 'created_at')
    list_display_links = ('product',)
    list_filter = ('rating', 'created_by', 'created_at')
    search_fields = ('product', 'created_by', 'created_at')


admin.site.register(Review, ReviewAdmin)
