# from django.contrib import admin
# from .models import Post, Comment, Vote, Restaurant

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'date_posted', 'upvotes', 'downvotes', 'resto')
#     search_fields = ('title', 'content', 'author__username', 'resto__name')
#     list_filter = ('date_posted', 'resto')

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'author', 'date_posted')
#     search_fields = ('content', 'author__username', 'post__title')
#     list_filter = ('date_posted',)

# @admin.register(Vote)
# class VoteAdmin(admin.ModelAdmin):
#     list_display = ('post', 'user', 'vote_type')
#     search_fields = ('user__username', 'post__title')
#     list_filter = ('vote_type',)

# @admin.register(Restaurant)
# class RestaurantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'city', 'district', 'place', 'unique_menu', 'price', 'google_rating', 'google_count', 'platform_rating', 'platform_count')
#     search_fields = ('name', 'city', 'district', 'place', 'unique_menu')
#     list_filter = ('city', 'district', 'place')
