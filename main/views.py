from django.shortcuts import render, redirect
from django.http import HttpResponse

#Form
from main.forms import RestaurantForm

# Models
from resto.models import Restaurant

# Serializer
from django.core import serializers

# Auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Date for Session
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# CSRF and Security
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

@login_required(login_url='main:user_login')
def main_page(request):
    # restaurants = Restaurant.objects.all()
    context = {
        'user' : request.user,
    }
    return render(request, 'main_page.html', context)

def search_restaurants(request):
    query = request.GET.get('q', '').strip()
    
    # Validate input length and content
    if len(query) > 100:  # Limit input length to prevent overly long queries
        return HttpResponseBadRequest("Invalid query length")
    
    if query:
        # Filter restaurants by name, making sure the query is secure by using Django ORM methods
        restaurants = Restaurant.objects.filter(name__icontains=query)
    else:
        restaurants = Restaurant.objects.all()
    
    results = [
        {
            'id': restaurant.id,
            'name': restaurant.name,
            'location': restaurant.location,
            'rating': restaurant.rating,
            'description': restaurant.description,
            'price': restaurant.price,
            'opening_time': restaurant.opening_time,
            'closing_time': restaurant.closing_time,
        }
        for restaurant in restaurants
    ]
    
    return JsonResponse({'restaurants': results})

# Product Management
def delete_resto(request, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return redirect('main:main_page')

def edit_resto(request, id):
    restaurant = Restaurant.objects.get(id = id)

    form = RestaurantForm(request.POST or None, instance=restaurant)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:main_page'))

    context = {'form': form}
    return render(request, "edit_resto.html", context)

def add_resto(request):
    form = RestaurantForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:main_page')

    context = {'form': form}
    return render(request, "create_resto.html", context)

# Auth
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:main_page"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def user_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:user_login')
        else :
            messages.error(request, 'Error creating your account')
    context = {'form':form}
    return render(request, 'register.html', context)

def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:user_login'))
    response.delete_cookie('last_login')
    return response

def show_json(request):
    restaurants = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", restaurants), content_type="application/json")