from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response, reverse('home'))

    def tearDown(self):
        self.user.delete()
