from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import serializers
from django.views.decorators.http import require_POST
import json

# Models
from resto.models import Restaurant
from resto_rating.models import Review
from reservation.models import Reservation
from wishlist.models import WishlistCategory, WishlistItem

@login_required(login_url='authentication:user_login')
def main_page(request):
    restaurants = Restaurant.objects.all()
    context = {
        'user': request.user,
        'restaurants': restaurants,
    }
    return render(request, 'main/main_page.html', context)

def about_page(request):
    return render(request, 'main/about_page.html')

def show_json(request):
    restaurants = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", restaurants), content_type="application/json")

def show_json_by_id(request, id):
    restaurant = Restaurant.objects.get(id=id)
    return HttpResponse(serializers.serialize("json", restaurant), content_type="application/json")
    
@login_required(login_url='authentication:user_login')
def steakhouse_page(request, pk):
    steakhouse = get_object_or_404(Restaurant, id=pk)
    reviews = Review.objects.filter(restaurant=steakhouse)
    reservations = Reservation.objects.filter(user=request.user, restaurant=steakhouse)

    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(restaurant=steakhouse, user=request.user).exists()

    context = {
        'steakhouse': steakhouse,
        'reviews': reviews,
        'reservations': reservations,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'main/steakhouse_page.html', context)

