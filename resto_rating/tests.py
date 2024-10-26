from django.test import TestCase
from django.contrib.auth.models import User
from resto.models import Restaurant
from resto_rating.models import Review
from django.core.exceptions import ValidationError

class ReviewModelTests(TestCase):
    def setUp(self):
        # Buat pengguna dan restoran uji untuk pengujian
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.restaurant = Restaurant.objects.create(
            id=1,
            name='Test Steakhouse',
            price=100,
            location='Downtown',
            special_menu='Ribeye',
            rating=4,
            description='Great steak and wine selection.',
            opening_time='10:00:00',
            closing_time='22:00:00'
        )

    def test_create_review(self):
        # Uji membuat ulasan yang valid
        review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=5,
            comment='Amazing food!'
        )
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Amazing food!')
        self.assertIsNotNone(review.created_at)  # Periksa apakah created_at diatur

    def test_invalid_rating(self):
        # Uji bahwa ulasan tidak dapat dibuat dengan rating yang tidak valid
        invalid_review = Review(
            restaurant=self.restaurant,
            user=self.user,
            rating=6,  # Rating tidak valid, harus 1-5
            comment='Good steak.'
        )
        with self.assertRaises(ValidationError):
            invalid_review.full_clean()  # Ini harus memunculkan kesalahan validasi

    def test_unique_constraint(self):
        # Buat ulasan
        Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            rating=4,
            comment='Nice place!'
        )

        # Coba buat ulasan lain untuk restoran yang sama oleh pengguna yang sama
        duplicate_review = Review(
            restaurant=self.restaurant,
            user=self.user,
            rating=5,
            comment='Loved it!'
        )
        with self.assertRaises(ValidationError):
            duplicate_review.full_clean()  # Ini harus memunculkan kesalahan validasi
