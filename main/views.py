from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

#Form
from main.forms import RestaurantForm, ReservationForm

# Models
from resto.models import Restaurant
from resto_rating.models import Review 
from reservation.models import Reservation

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
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

@login_required(login_url='main:user_login')
def main_page(request):
    restaurants = Restaurant.objects.all()
    context = {
        'user' : request.user,
        'restaurants' : restaurants,
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

def steakhouse_page(request, pk):
    steakhouse = Restaurant.objects.get(id=pk)
    reviews = Review.objects.filter(restaurant=steakhouse)
    
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(restaurant=steakhouse, user=request.user).exists()
    
    context = {
        'steakhouse': steakhouse,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'steakhouse_page.html', context)

# Code for resto_rating application
def add_review(request, restaurant_id):
    if request.method == 'POST':
        restaurant = Restaurant.objects.get(id=restaurant_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            restaurant=restaurant,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        return redirect('main:steakhouse_page', pk=restaurant_id)
    
    return redirect('main:steakhouse_page', pk=restaurant_id)

@require_POST
def edit_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        
        if request.user != review.user and not request.user.is_superuser:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        data = json.loads(request.body)
        review.rating = data.get('rating')
        review.comment = data.get('comment')
        review.save()
        
        return JsonResponse({'message': 'Review updated successfully'})
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        
        if request.user != review.user and not request.user.is_superuser:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        review.delete()
        return JsonResponse({'message': 'Review deleted successfully'})
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
# Code for resevation application
@login_required(login_url='main:user_login')
def make_reservation(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.restaurant = restaurant
            
            # Cek apakah pengguna sudah memiliki reservasi aktif di restoran ini
            if Reservation.objects.filter(user=request.user, restaurant=restaurant, status='active').exists():
                messages.error(request, 'Anda sudah memiliki reservasi aktif di restoran ini. Selesaikan reservasi sebelumnya untuk membuat yang baru.')
                return redirect('main:steakhouse_page', pk=restaurant.id)
            
            reservation.save()
            messages.success(request, 'Reservasi berhasil dibuat!')
            return redirect('main:steakhouse_page', pk=restaurant.id)
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'restaurant': restaurant,
    }
    return render(request, 'make_reservation.html', context)

@login_required(login_url='main:user_login')
def complete_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        reservation.status = 'completed'
        reservation.save()
        messages.success(request, 'Reservasi telah diselesaikan.')
    except Reservation.DoesNotExist:
        messages.error(request, 'Reservasi tidak ditemukan atau Anda tidak memiliki akses.')

    return redirect('main:steakhouse_page')

@login_required(login_url='main:user_login')
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    context = {
        'reservations': reservations,
    }
    return render(request, 'steakhouse_page.html', context) 
