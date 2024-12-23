from django.test import TestCase, Client
from django.urls import reverse
from resto.models import Restaurant
from django.core.exceptions import ValidationError

class RestaurantSearchTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        # Membuat restoran sampel untuk pengujian
        Restaurant.objects.create(
            id=1,
            name='Steakhouse A',
            price=150,
            location='Downtown',
            special_menu='Grilled Steak',
            rating=4,
            description='Steak terbaik di kota.',
            opening_time='10:00:00',
            closing_time='22:00:00'
        )
        Restaurant.objects.create(
            id=2,
            name='Steakhouse B',
            price=200,
            location='Uptown',
            special_menu='Ribeye Steak',
            rating=5,
            description='Steak berkualitas premium.',
            opening_time='11:00:00',
            closing_time='23:00:00'
        )

    def test_search_restaurants_valid_query(self):
        # Menguji pencarian dengan query yang valid
        response = self.client.get(reverse('resto:search_restaurants'), {'q': 'Steakhouse A'})
        self.assertEqual(response.status_code, 200) # Harus mengembalikan status OK
        
        data = response.json()
        self.assertEqual(len(data['restaurants']), 1)
        self.assertEqual(data['restaurants'][0]['name'], 'Steakhouse A')

    def test_search_restaurants_no_results(self):
        # Menguji pencarian dengan query yang tidak menghasilkan hasil
        response = self.client.get(reverse('resto:search_restaurants'), {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data['restaurants']), 0)

    def test_search_restaurants_long_query(self):
        # Menguji pencarian dengan query panjang yang melebihi batas
        long_query = 'x' * 101  # Membuat query lebih dari 100 karakter
        response = self.client.get(reverse('resto:search_restaurants'), {'q': long_query})
        self.assertEqual(response.status_code, 400)  # Mengharapkan respons Bad Request

    def test_search_restaurants_empty_query(self):
        # Menguji pencarian dengan query kosong
        response = self.client.get(reverse('resto:search_restaurants'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data['restaurants']), 2)  # Harus mengembalikan semua restoran

    def test_search_restaurants_case_insensitivity(self):
        # Menguji pencarian dengan case yang berbeda
        response = self.client.get(reverse('resto:search_restaurants'), {'q': 'steakhouse a'})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data['restaurants']), 1)
        self.assertEqual(data['restaurants'][0]['name'], 'Steakhouse A')


class RestaurantModelTests(TestCase):
    def setUp(self):
        # Membuat instance restoran untuk pengujian
        self.restaurant = Restaurant.objects.create(
            id=1,
            name="Test Steakhouse",
            price=150,
            location="Downtown",
            special_menu="Ribeye Steak",
            description="Tempat yang bagus untuk pecinta steak.",
            opening_time="08:00:00",
            closing_time="21:00:00"
        )

    def test_restaurant_creation(self):
        # Menguji apakah restoran berhasil dibuat
        self.assertEqual(self.restaurant.name, "Test Steakhouse")
        self.assertEqual(self.restaurant.price, 150)
        self.assertEqual(self.restaurant.location, "Downtown")
        self.assertEqual(self.restaurant.special_menu, "Ribeye Steak")
        self.assertEqual(self.restaurant.description, "Tempat yang bagus untuk pecinta steak.")
        self.assertEqual(str(self.restaurant.opening_time), "08:00:00")
        self.assertEqual(str(self.restaurant.closing_time), "21:00:00")

    def test_restaurant_default_values(self):
        # Menguji nilai default untuk deskripsi
        default_restaurant = Restaurant.objects.create(
            id=2,
            name="Another Steakhouse",
            price=200,
            location="Uptown",
            special_menu="Sirloin Steak"
        )
        
        self.assertEqual(default_restaurant.description, "Steak house with a variety of dishes and a great view of the city")  # Memeriksa deskripsi default

    def test_invalid_price(self):
        # Menguji bahwa restoran tidak dapat dibuat dengan harga yang tidak valid (kurang dari 1)
        invalid_restaurant = Restaurant(
            id=3,
            name="Invalid Price Steakhouse",
            price=-100,  # Harga tidak valid
            location="Midtown",
            special_menu="T-bone Steak"
        )
        
        with self.assertRaises(ValidationError) as context:
            invalid_restaurant.full_clean()  # Validasi, jika ada yang gagal maka akan melempar ValidationError
        
        self.assertTrue('Ensure this value is greater than or equal to 1.' in str(context.exception))

    def test_edit_restaurant(self):
        # Menguji pengeditan restoran yang ada
        self.restaurant.name = "Updated Steakhouse"
        self.restaurant.price = 180
        self.restaurant.save()

        # Memuat ulang restoran dari database
        self.restaurant.refresh_from_db()

        #Cek apakah restoran telah diupdate
        self.assertEqual(self.restaurant.name, "Updated Steakhouse")
        self.assertEqual(self.restaurant.price, 180)

    def test_delete_restaurant(self):
        # Menguji penghapusan restoran yang ada
        self.restaurant.delete()
        with self.assertRaises(Restaurant.DoesNotExist):
            Restaurant.objects.get(id=self.restaurant.id)  # Memeriksa bahwa restoran telah dihapus
