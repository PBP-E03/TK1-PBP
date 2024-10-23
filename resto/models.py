from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    description = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField() 