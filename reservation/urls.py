from django.urls import path
from reservation.views import *

app_name = 'reservation'

urlpatterns = [
    path('complete_reservation/<int:reservation_id>/', complete_reservation, name='complete_reservation'),
    path('<int:restaurant_id>/', make_reservation, name='make_reservation'),
    path('', user_reservations, name='user_reservations'),
]