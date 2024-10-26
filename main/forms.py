from django.forms import ModelForm
from resto.models import Restaurant 

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "location", "price", "special_menu","description", "opening_time", "closing_time"]