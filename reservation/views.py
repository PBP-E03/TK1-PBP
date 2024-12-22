from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

# Form and Model
from reservation.forms import ReservationForm
from resto.models import Restaurant
from reservation.models import Reservation


@login_required(login_url='authentication:user_login')
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
    return render(request, 'reservation/make_reservation.html', context)


@login_required(login_url='authentication:user_login')
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    context = {
        'reservations': reservations,
    }
    return render(request, 'user_reservations.html', context)

@login_required(login_url='authentication:user_login')
def complete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if reservation.status in ['completed', 'canceled']:
        return JsonResponse({'error': 'Reservation cannot be completed again.'}, status=400)

    reservation.status = 'completed'
    reservation.save()

    messages.success(request, 'Reservation completed successfully.')
    return JsonResponse({'message': 'Reservation completed successfully.'})

@csrf_exempt
@require_POST
def edit_reservation(request, reservation_id):
    try:
        data = json.loads(request.body)
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

        if reservation.status in ['completed', 'canceled']:
            return JsonResponse({'error': 'Reservation cannot be edited once it is completed or canceled.'}, status=400)

        # Validate inputs
        date = data.get('date')
        time = data.get('time')
        if not date or not time:
            return JsonResponse({'error': 'Date and time are required.'}, status=400)
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            datetime.datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            return JsonResponse({'error': 'Invalid date or time format. Use YYYY-MM-DD and HH:MM:SS.'}, status=400)

        # Update reservation
        reservation.date = date
        reservation.time = time
        reservation.special_request = data.get('special_request', reservation.special_request)
        reservation.save()

        return JsonResponse({'message': 'Reservation updated successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    
@csrf_exempt
@require_POST
def delete_reservation(request, reservation_id):
    try:
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

        if reservation.status in ['completed', 'canceled']:
            return JsonResponse({'error': 'Reservation cannot be deleted once it is completed or canceled.'}, status=400)

        reservation.status = 'canceled'
        reservation.save()

        return JsonResponse({'message': 'Reservation canceled successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def create_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            required_fields = ['user_id', 'restaurant_id', 'name', 'date', 'time', 'guests', 'contact_info']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return JsonResponse({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

            # Validate date and time formats
            try:
                datetime.datetime.strptime(data['date'], '%Y-%m-%d')
                datetime.datetime.strptime(data['time'], '%H:%M:%S')
            except ValueError:
                return JsonResponse({'error': 'Invalid date or time format. Use YYYY-MM-DD and HH:MM:SS.'}, status=400)

            # Check for existing active reservation
            if Reservation.objects.filter(
                user_id=data['user_id'], 
                restaurant_id=data['restaurant_id'], 
                status='active'
            ).exists():
                return JsonResponse({'error': 'An active reservation already exists for this user at this restaurant.'}, status=400)

            # Create reservation
            reservation = Reservation.objects.create(
                user_id=data['user_id'],
                restaurant_id=data['restaurant_id'],
                name=data['name'],
                date=data['date'],
                time=data['time'],
                guests=data['guests'],
                contact_info=data['contact_info'],
                special_request=data.get('special_request', ''),
                status='active',
            )
            return JsonResponse({'message': 'Reservation created successfully', 'reservation_id': reservation.id}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)
    return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)