from django.urls import include, path
from resto.views import *

app_name = 'resto'
urlpatterns = [
    path('add-resto/', add_resto, name='add_resto'),
    path('edit-resto/<int:id>/', edit_resto, name='edit_resto'),
    path('delete-resto/<int:id>/', delete_resto, name='delete_resto'),
    path('search/', search_restaurants, name='search_restaurants'),
]