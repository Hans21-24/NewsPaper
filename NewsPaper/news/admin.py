from django.contrib import admin
from .models import *


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'heading', 'date_created', 'category_type', 'author', 'rating')
    list_display_links = ('id', 'heading', 'category_type', 'author')
    search_fields = ('category_type', 'author')
    list_filter = ('category_type', 'date_created', 'author')
    inlines = [PostCategoryInLine]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', )
    inlines = [PostCategoryInLine]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
