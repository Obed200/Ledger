from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "featured", "created_at")
    list_filter = ("category", "featured")
    search_fields = ("title", "dek", "body")
    prepopulated_fields = {"slug": ("title",)}
