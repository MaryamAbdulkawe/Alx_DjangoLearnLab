from django.contrib import admin
from .models import Post, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
