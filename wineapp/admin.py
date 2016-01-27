from django.contrib import admin

from .models import Wine, Review, Post


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'user_name', 'text', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['text']


admin.site.register(Wine)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Post, PostAdmin)
