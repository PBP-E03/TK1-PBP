from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from resto.models import Restaurant

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    restaurant = models.ForeignKey(Restaurant, related_name='reservations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    contact_info = models.CharField(max_length=100)
    special_request = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f'Reservation for {self.name} at {self.restaurant.name} on {self.date}'


# Create your models here.
