from django.forms import ModelForm
from resto.models import Restaurant 
from reservation.models import Reservation

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "location", "price", "description", "opening_time", "closing_time"]

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'date', 'time', 'number_of_guests', 'contact_info', 'special_request', 'status']
