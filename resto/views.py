from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse

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