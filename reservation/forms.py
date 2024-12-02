from django.forms import ModelForm
from reservation.models import Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'date', 'time', 'number_of_guests', 'contact_info', 'special_request', 'status']
