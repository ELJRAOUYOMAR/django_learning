from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Admin intefrace for Post model """
    list_display = ('title', 'author', 'status', 'category', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at', )