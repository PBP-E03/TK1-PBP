from django.test import TestCase, Client
from resto.models import Restaurant
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTests(TestCase):
    
    # Membuat User
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_registration(self):
        # Menguji Registrasi User
        response = self.client.post(reverse('authentication:user_register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        
        # Memeriksa bahwa user dibuat dan diarahkan ke halaman login
        self.assertEqual(response.status_code, 302)  # 302 adalah kode status redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        # Menguji Login User
        response = self.client.post(reverse('authentication:user_login'), {
            'username': self.username,
            'password': self.password
        })
        
        # Memeriksa bahwa user login dan diarahkan
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(str(response.wsgi_request.user), str(self.user))

    def test_invalid_user_login(self):
        # Menguji Login yang Tidak Valid
        response = self.client.post(reverse('authentication:user_login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })

        # Memeriksa bahwa login gagal dan kembali ke halaman login
        self.assertEqual(response.status_code, 200)  # 200 adalah kode Status Harus merender halaman login lagi
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_login_redirect(self):
        # Menguji bahwa user yang terautentikasi diarahkan ke halaman utama
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('authentication:user_login'))

        # Memastikan user diarahkan ke halaman utama
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:main_page'))