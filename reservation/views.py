from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

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
    reservations = Reservation.objects.filter(user=request.user)
    context = {
        'reservations': reservations,
    }
    return render(request, 'user_reservations.html', context)

@login_required(login_url='authentication:user_login')
def complete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.status = 'completed'
    reservation.save()
    messages.success(request, 'Reservation completed successfully.')
    
    return JsonResponse({'message': 'Reservation completed successfully.'})
