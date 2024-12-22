from django.urls import path
from resto_rating.views import *    

app_name = 'resto_rating'

urlpatterns = [
    path('add_review/<int:restaurant_id>/', add_review, name='add_review'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),

    path('flutter/get_rating/<int:restaurant_id>/', get_rating, name='get_rating'),
    path('flutter/add_review/<int:restaurant_id>/', flutter_add_review, name='flutter_add_review'),
    path('flutter/edit_review/<int:review_id>/', flutter_edit_review, name='flutter_edit_review'),
    path('flutter/delete_review/<int:review_id>/', flutter_delete_review, name='flutter_delete_review')
]