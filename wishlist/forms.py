from django import forms
from .models import WishlistItem, WishlistCategory

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['title', 'wishlistCategory']

class WishlistCategoryForm(forms.ModelForm):
    class Meta:
        model = WishlistCategory
        fields = ['name', 'description']
