from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Restaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)    
    price = models.IntegerField(validators=[MinValueValidator(1)])
    location = models.CharField(max_length=100)
    special_menu = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default = 0
    )
    description = models.TextField(default= "Steak house with a variety of dishes and a great view of the city")
    opening_time = models.TimeField(default="07:00:00")
    closing_time = models.TimeField(default = "22:00:00") 

    def __str__(self):
        return self.name