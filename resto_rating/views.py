from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
import json
from django.views.decorators.http import require_POST

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
