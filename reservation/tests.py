from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Reservation

class ReservationViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.reservation = Reservation.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            name='Test Reservation',
            date='2024-10-30',
            status='active'
        )

    def test_make_reservation_success(self):
        """Test that a user can make a reservation successfully."""
        response = self.client.post(reverse('main:make_reservation', args=[self.restaurant.id]), {
            'name': 'New Reservation',
            'date': '2024-11-01',
            'quantity': 2,
            'contact': 'test@example.com'
        })

        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Reservation.objects.count(), 2)  
        self.assertTrue(Reservation.objects.filter(name='New Reservation').exists())  

    def test_make_reservation_already_active(self):
        """Test that a user cannot make a new reservation if one is already active."""
        response = self.client.post(reverse('main:make_reservation', args=[self.restaurant.id]), {
            'name': 'Another Reservation',
            'date': '2024-11-02',
            'quantity': 2,
            'contact': 'test@example.com'
        })

        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Reservation.objects.count(), 1) 
        self.assertContains(response, 'You already have an active reservation')

    def test_complete_reservation(self):
        """Test that a user can complete a reservation successfully."""
        response = self.client.post(reverse('main:complete_reservation', args=[self.reservation.id]))

        self.reservation.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.reservation.status, 'completed')
        self.assertContains(response, 'Reservation completed successfully.')

    def test_user_reservations(self):
        """Test that the user can view their reservations."""
        response = self.client.get(reverse('main:user_reservations'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Reservation')

# Create your tests here.
