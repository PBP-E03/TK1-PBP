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
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    description = models.TextField(default= "Steak house with a variety of dishes")
    opening_time = models.TimeField(default="07:00:00")
    closing_time = models.TimeField(default = "22:00:00") 