from django.db import models
from django.contrib.auth.models import User
from resto.models import Restaurant
from django.core.validators import MaxValueValidator, MinValueValidator

class WishlistCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlistCategory")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class WishlistItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='wishlist', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    wishlistCategory = models.ForeignKey(WishlistCategory, on_delete=models.CASCADE, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)