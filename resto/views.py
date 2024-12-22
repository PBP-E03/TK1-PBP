from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import json

# Forms
from resto.forms import RestaurantForm

# Models
from resto.models import Restaurant

def delete_resto(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurant.delete()
    return redirect('main:main_page')

def edit_resto(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    form = RestaurantForm(request.POST or None, instance=restaurant)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:main_page'))

    context = {'form': form}
    return render(request, "resto/edit_resto.html", context)

def add_resto(request):
    form = RestaurantForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:main_page')

    context = {'form': form}
    return render(request, "resto/create_resto.html", context)

def search_restaurants(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) > 100:
        return HttpResponseBadRequest("Invalid query length")
    
    if query:
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
            'special_menu': restaurant.special_menu,
            'price': restaurant.price,
            'opening_time': restaurant.opening_time,
            'closing_time': restaurant.closing_time,
        }
        for restaurant in restaurants
    ]
    return JsonResponse({'restaurants': results})

# Flutter
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", restaurants), content_type="application/json")

@csrf_exempt
def create_restaurant_flutter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_resto = Restaurant(
                name=data['name'],
                location=data['address'],
                description=data['description'],
                special_menu=data['special_menu'],
                price=data['price'],
                opening_time=data['open_time'],
                closing_time=data['close_time']   
            )
            new_resto.save()
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'}, status=400)
        
        if request.user.is_authenticated:
            print(request.user)
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failed'}, status=400)

@csrf_exempt
def delete_restaurant_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            delete_resto = get_object_or_404(Restaurant, id=data['id'])
            delete_resto.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'}, status = 400)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status = 400)

@csrf_exempt
def edit_restaurant_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_resto = Restaurant(
                name=data['name'],
                location=data['address'],
                description=data['description'],
                special_menu=data['special_menu'],
                price=data['price'],
                opening_time=data['open_time'],
                closing_time=data['close_time']   
            )
            edited_restaurant = get_object_or_404(Restaurant, id=data['id'])

            # Update the restaurant
            edited_restaurant.name = new_resto.name
            edited_restaurant.location = new_resto.location
            edited_restaurant.description = new_resto.description
            edited_restaurant.special_menu = new_resto.special_menu
            edited_restaurant.price = new_resto.price
            edited_restaurant.opening_time = new_resto.opening_time
            edited_restaurant.closing_time = new_resto.closing_time
            
            edited_restaurant.save()
            # print(request.user)
            return JsonResponse({'status': 'success'}, status=200)
            
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'}, status=400)
    return JsonResponse({'status': 'failed'}, status=400)