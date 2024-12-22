from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core import serializers
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Model
from resto.models import Restaurant
from resto_rating.models import Review

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
        update_restaurant_rating(restaurant)
        
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
        update_restaurant_rating(review.restaurant)
        
        return JsonResponse({'message': 'Review updated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user != review.user and not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    restaurant = review.restaurant
    review.delete()

    # Update the restaurant's rating
    update_restaurant_rating(restaurant)

    return JsonResponse({'message': 'Review deleted successfully'})

def update_restaurant_rating(restaurant):
    reviews = Review.objects.filter(restaurant=restaurant)
    if reviews.exists():
        total_rating = sum(r.rating for r in reviews)
        restaurant.rating = total_rating / reviews.count()
    else:
        restaurant.rating = 0
    restaurant.save()

def get_rating(request, restaurant_id):
    reviews = Review.objects.filter(restaurant_id=restaurant_id)
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

@csrf_exempt
def flutter_add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        try:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
            
            data = json.loads(request.body)
            rating = data.get('rating')
            comment = data.get('comment')

            if not rating:
                return JsonResponse({'error': 'Missing rating'}, status=400)

            if not (1 <= int(rating) <= 5):
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

            # Create the review
            Review.objects.create(
                restaurant=restaurant,
                user=user,
                rating=rating,
                comment=comment
            )

            # Update restaurant's average rating
            update_restaurant_rating(restaurant)

            return JsonResponse({'message': 'Review added successfully', 'new_rating': restaurant.rating}, status=201)
        except (ValueError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def flutter_edit_review(request, review_id):
    if request.method == 'PUT':
        try:
            review = get_object_or_404(Review, id=review_id)
            
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            data = json.loads(request.body)
            rating = data.get('rating')
            comment = data.get('comment')

            if not rating:
                return JsonResponse({'error': 'Missing rating'}, status=400)

            if not (1 <= int(rating) <= 5):
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

            if review.user != user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            # Update review
            review.rating = rating
            review.comment = comment
            review.save()

            # Update restaurant's average rating
            update_restaurant_rating(review.restaurant)

            return JsonResponse({'message': 'Review updated successfully', 'new_rating': review.restaurant.rating}, status=200)
        except (ValueError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def flutter_delete_review(request, review_id):
    if request.method == 'DELETE':
        try:
            # Access authenticated user directly
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            # Fetch the review
            review = get_object_or_404(Review, id=review_id)

            # Check if the user is authorized to delete the review
            if review.user != user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            # Delete the review
            restaurant = review.restaurant
            review.delete()

            # Update restaurant's average rating
            update_restaurant_rating(restaurant)

            return JsonResponse({'message': 'Review deleted successfully', 'new_rating': restaurant.rating}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
