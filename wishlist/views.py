from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import WishlistCategory, WishlistItem
from resto.models import Restaurant
from .forms import WishlistItemForm, WishlistCategoryForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import json

def view_wishlists(request):
    categorized_wishlists = {}
    selected_category = None  # To store the currently selected category

    if request.user.is_authenticated:
        wishlists = WishlistItem.objects.filter(user=request.user).select_related('restaurant', 'wishlistCategory')

        categories = WishlistCategory.objects.filter(user=request.user)

        if 'category' in request.GET:
            selected_category_id = request.GET['category']
            selected_category = categories.filter(id=selected_category_id).first()  # Get the selected category
            if selected_category:
                wishlists = wishlists.filter(wishlistCategory=selected_category)

        for category in categories:
            items = wishlists.filter(wishlistCategory=category)
            if items.exists():  
                categorized_wishlists[category] = items

    context = {
        'categorized_wishlists': categorized_wishlists,
        'categories': categories,  
        'selected_category': selected_category,  
    }
    return render(request, 'view_wishlists.html', context)