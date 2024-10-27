from django.urls import path
from . import views

urlpatterns = [
    path('wishlists/', views.view_wishlists, name='view_wishlists'),
    path('wishlists/edit/<int:id>/', views.edit_wishlist, name='edit_wishlist'),
    path('wishlists/delete/<int:id>/', views.delete_wishlist, name='delete_wishlist'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),
]
