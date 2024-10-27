from django.urls import path
from . import views

urlpatterns = [
    # path('wishlist/create-category/', views.create_wishlist_category, name='create_wishlist_category'),
    # path('wishlist/edit/<int:item_id>/', views.edit_wishlist_item, name='edit_wishlist_item'),
    # path('wishlist/move/<int:item_id>/', views.move_wishlist_item, name='move_wishlist_item'),
    # path('wishlist/delete/<int:item_id>/', views.delete_wishlist_item, name='delete_wishlist_item'),
    path('wishlists/', views.view_wishlists, name='view_wishlists'),
]
