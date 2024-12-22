from django.urls import path
from reservation.views import *

app_name = 'reservation'

urlpatterns = [
    path('complete_reservation/<int:reservation_id>/', complete_reservation, name='complete_reservation'),
    path('<int:restaurant_id>/', make_reservation, name='make_reservation'),
    path('', user_reservations, name='user_reservations'),
    path('edit_reservation/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),

    
    path('api/reservations/create/', create_reservation, name='create_reservation'),
    path('reservation/flutter/edit-reservation/', edit_reservation, name='edit_reservation'),
    path('reservation/flutter/delete-reservation/', delete_reservation, name='delete_reservation'),
]