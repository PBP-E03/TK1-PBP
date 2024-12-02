from django.urls import path
from wishlist.views import *

app_name = 'wishlist'

urlpatterns = [
    path('', view_wishlists, name='view_wishlists'),
    path('edit/<int:id>/', edit_wishlist, name='edit_wishlist'),
    path('delete/<int:id>/', delete_wishlist, name='delete_wishlist'),
    path('delete-category/<int:id>/', delete_category, name='delete_category'),
    
    path('add/<int:restaurant_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('fetch-user-categories/', fetch_user_categories, name='fetch_user_categories'),

]
