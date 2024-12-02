from django.urls import path
from resto_rating.views import *    

app_name = 'resto_rating'

urlpatterns = [
    path('add_review/<int:restaurant_id>/', add_review, name='add_review'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
]