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
    selected_category = None  # Store the currently selected category
    categories = []

    if request.user.is_authenticated:
        wishlists = WishlistItem.objects.filter(user=request.user).select_related('restaurant', 'wishlistCategory')
        categories = WishlistCategory.objects.filter(user=request.user)

        # Check if a category is selected and is valid
        selected_category_id = request.GET.get('category')
        if selected_category_id:
            try:
                # Attempt to get the selected category if ID is valid
                selected_category = categories.get(id=selected_category_id)
                wishlists = wishlists.filter(wishlistCategory=selected_category)
            except WishlistCategory.DoesNotExist:
                # If the selected category does not exist, ignore filtering
                pass

        # Group items by their categories
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

@require_POST
def edit_wishlist(request, id):
    try:
        wishlistItem = WishlistItem.objects.get(id=id)
        
        if request.user != wishlistItem.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        data = json.loads(request.body)
        new_title = data.get('title')
        category_id = data.get('category_id')  
        new_category_name = data.get('new_category_name')   
        
        if new_title:
            wishlistItem.title = new_title
        
        if new_category_name:
            wishlistItem.wishlistCategory = WishlistCategory.objects.create(name=new_category_name, user=request.user)
        else:
            wishlistItem.wishlistCategory = get_object_or_404(WishlistCategory, id=category_id, user=request.user)
            
        wishlistItem.save()

        return JsonResponse({'message': 'Wishlist item updated successfully'})

    except WishlistItem.DoesNotExist:
        return JsonResponse({'error': 'Wishlist item not found'}, status=404)
    except WishlistCategory.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def delete_wishlist(request, id):
    try:
        wishlistItem = WishlistItem.objects.get(id=id)
        
        if request.user != wishlistItem.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        wishlistItem.delete()
        return JsonResponse({'message': 'Review deleted successfully'})
    except WishlistItem.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@require_POST
def delete_category(request, id):
    try:
        category = WishlistCategory.objects.get(id=id, user=request.user)
        category.delete()
        return JsonResponse({'message': 'Category deleted successfully'})
    except WishlistCategory.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Pindahan dari main/views.py

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