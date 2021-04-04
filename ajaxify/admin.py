from django.contrib import admin

from .models import Post, Category

from ajaxify.forms import PostForm


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'created_on', 'published_date')
    list_filter = ('created_on', 'last_modified', 'published_date')
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    form = PostForm
    fields = ['title', 'slug', 'summary', 'description', 'main_image', 'categories', 'published_date', 'likes', 'is_featured']
    

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)