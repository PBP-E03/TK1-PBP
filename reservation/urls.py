from django.urls import path
from reservation.views import *

app_name = 'reservation'

urlpatterns = [
    path('complete_reservation/<int:reservation_id>/', complete_reservation, name='complete_reservation'),
    path('<int:restaurant_id>/', make_reservation, name='make_reservation'),
    path('', user_reservations, name='user_reservations'),
    path('edit_reservation/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),

    
    path('create/', create_reservation, name='create_reservation'),
    path('edit/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('complete/<int:reservation_id>/', complete_reservation, name='complete_reservation')
]