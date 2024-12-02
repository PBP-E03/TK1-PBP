from django.contrib import admin
from django.urls import include, path
from main.views import *

app_name = 'main'
urlpatterns = [
    path('', main_page, name='main_page'),
    path('show-json/', show_json, name='show_json'),

    path('steakhouse/<int:pk>/', steakhouse_page, name='steakhouse_page'),

    path('forum_diskusi/', include('forum_diskusi.urls', namespace='forum_diskusi')),
    path('about/', about_page, name='about_page'),    
]