from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from resto.models import Restaurant

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant', 'user') 

    def __str__(self):
        return f'Review by {self.user.username} for {self.restaurant.name}'
    
    
    