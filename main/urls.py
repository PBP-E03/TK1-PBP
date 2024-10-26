from django.contrib import admin
from django.urls import path
from main.views import *

app_name = 'main'
urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
    path('show-json/', show_json, name='show_json'),
    
    path('add-resto/', add_resto, name='add_resto'),
    path('edit-resto/<int:id>/', edit_resto, name='edit_resto'),
    path('delete-resto/<int:id>/', delete_resto, name='delete_resto'),

    path('steakhouse/<int:pk>/', steakhouse_page, name='steakhouse_page'),
    path('add_review/<int:restaurant_id>/', add_review, name='add_review'),
    path('edit_review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('search/', search_restaurants, name='search_restaurants'),

    path('reservation/make/<int:restaurant_id>/', make_reservation, name='make_reservation'),
    path('reservation/complete/<int:reservation_id>/', complete_reservation, name='complete_reservation'),
    path('reservations/', user_reservations, name='user_reservations'),
]