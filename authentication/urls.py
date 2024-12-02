from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
]