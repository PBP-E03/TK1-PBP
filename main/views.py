from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
import json
import datetime
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Forms
from main.forms import RestaurantForm, ReservationForm

# Models
from resto.models import Restaurant
from resto_rating.models import Review
from reservation.models import Reservation
from wishlist.models import WishlistCategory, WishlistItem

@login_required(login_url='main:user_login')
def main_page(request):
    restaurants = Restaurant.objects.all()
    context = {
        'user': request.user,
        'restaurants': restaurants,
    }
    return render(request, 'main_page.html', context)

def about_page(request):
    return render(request, 'about_page.html')

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
    return render(request, "edit_resto.html", context)

def add_resto(request):
    form = RestaurantForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:main_page')

    context = {'form': form}
    return render(request, "create_resto.html", context)

def user_login(request):
    # Redirect authenticated users to the main page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:main_page'))
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
        else:
            messages.error(request, 'Error creating your account')
    context = {'form': form}
    return render(request, 'register.html', context)

def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:user_login'))
    response.delete_cookie('last_login')
    return response

def show_json(request):
    restaurants = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", restaurants), content_type="application/json")

def show_json_by_id(request, id):
    restaurant = Restaurant.objects.get(id=id)
    return HttpResponse(serializers.serialize("json", restaurant), content_type="application/json")
    
@login_required(login_url='main:user_login')
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
    return render(request, 'steakhouse_page.html', context)

def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Create the review
        Review.objects.create(
            restaurant=restaurant,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        # Update the restaurant's rating
        reviews = Review.objects.filter(restaurant=restaurant)
        total_rating = sum(review.rating for review in reviews)
        restaurant.rating = total_rating / reviews.count()
        restaurant.save()
        
        return redirect('main:steakhouse_page', pk=restaurant_id)
    
    return redirect('main:steakhouse_page', pk=restaurant_id)

@require_POST
def edit_review(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        
        if request.user != review.user and not request.user.is_superuser:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        data = json.loads(request.body)
        review.rating = data.get('rating')
        review.comment = data.get('comment')
        review.save()
        
        # Update the restaurant's rating
        restaurant = review.restaurant
        reviews = Review.objects.filter(restaurant=restaurant)
        total_rating = sum(r.rating for r in reviews)
        restaurant.rating = total_rating / reviews.count()
        restaurant.save()
        
        return JsonResponse({'message': 'Review updated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user != review.user and not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    review.delete()
    return JsonResponse({'message': 'Review deleted successfully'})

@login_required(login_url='main:user_login')
def make_reservation(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.restaurant = restaurant

            if Reservation.objects.filter(user=request.user, restaurant=restaurant, status='active').exists():
                messages.error(request, 'You already have an active reservation at this restaurant. Please complete it before making a new one.')
                return redirect('main:steakhouse_page', pk=restaurant.id)

            reservation.save()
            messages.success(request, f'Reservation for {reservation.name} at {reservation.restaurant.name} on {reservation.date} made successfully!')
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
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.status = 'completed'
    reservation.save()
    messages.success(request, 'Reservation completed successfully.')
    
    return JsonResponse({'message': 'Reservation completed successfully.'})

@login_required(login_url='main:user_login')
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    context = {
        'reservations': reservations,
    }
    return render(request, 'user_reservations.html', context)


# Wishlist section
@login_required
def fetch_user_categories(request):
    categories = WishlistCategory.objects.filter(user=request.user).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

@require_POST
def add_to_wishlist(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    user = request.user

    data = json.loads(request.body) 
    title = data.get('title')
    category_id = data.get('category_id')  
    new_category_name = data.get('new_category_name')   

    if new_category_name:
        category = WishlistCategory.objects.create(name=new_category_name, user=user)
    else:
        category = get_object_or_404(WishlistCategory, id=category_id, user=user)

    new_wishlist = WishlistItem(
        restaurant=restaurant, user=user,
        title=title, wishlistCategory=category
    )
    new_wishlist.save()

    print("Title:", title)
    print("Category ID:", category_id)
    print("New Category Name:", new_category_name)
    return JsonResponse({'status': 'CREATED'}, status=201)
