from django import forms
from .models import WishlistItem, WishlistCategory

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['title', 'wishlistCategory']

class WishlistCategoryForm(forms.ModelForm):
    class Meta:
        model = WishlistCategory
<<<<<<< HEAD
        fields = ['name']
=======
        fields = ['name']
>>>>>>> 7dbd0c3b0f9c611c7e66aa5cb5564a48b1264a2d
