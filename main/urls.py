from django.contrib import admin
from django.urls import path
from main.views import *

app_name = 'main'
urlpatterns = [
    path('', main_page, name='main_page'),
]