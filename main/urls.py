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
]