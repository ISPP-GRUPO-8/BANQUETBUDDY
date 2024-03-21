from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser
from catering_owners.models import CateringCompany, CateringService
from catering_particular.models import Particular
from django.test import TestCase, Client


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    # Tests that the login view is retrieved correctly
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    # Tests that an authenticated user is redirected when attempting to access the login view
    def test_login_view_authenticated_user(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed("home")

    # Tests the login with valid credentials
    def test_login_view_valid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'test@example.com', 'password': 'testpassword'})
        self.assertTemplateUsed("home")
        self.assertTrue(self.client.session['_auth_user_id'])

    # Tests the login with invalid credentials
    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'test@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertFalse(self.client.session.get('_auth_user_id'))

class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertTemplateUsed("home")
    def tearDown(self):
        self.user.delete()

class ListarCateringsHomeTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear un usuario particular y datos asociados
        self.user_particular = CustomUser.objects.create_user(
            username="pablo@gmail.com", password="Pablo", email="pablo@gmail.com"
        )
        self.particular = Particular.objects.create(
            user=self.user_particular,
            phone_number="+123456789",
            preferences="Some preferences",
            address="Some address",
            is_subscribed=True,
        )

        # Crear un servicio de catering asociado al usuario particular
        self.catering_service = CateringService.objects.create(
            cateringcompany=CateringCompany.objects.create(
                user=self.user_particular,
                name="Catering Company 1",
                phone_number="+987654321",
                service_description="Some description",
                is_verified=True,
                price_plan="PREMIUM",
            ),
            name="Test Catering Service",
            description="Service description",
            location="Service location",
            capacity=100,
            price=1000.00,
        )

        # Autenticar al usuario particular
        self.client.login(username="pablo@gmail.com", password="Pablo")

    
    def test_busqueda_por_nombre_existente(self):
        response = self.client.post(reverse("listar_caterings"), {"buscar": "Test Catering Service"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Catering Service")
        self.assertNotContains(response, "Nonexistent Catering")

    def test_busqueda_por_nombre_vacio(self):
        response = self.client.post(reverse("listar_caterings"), {"buscar": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Catering Service")

    def tearDown(self) -> None:
        self.user_particular.delete()
        self.particular.delete()
        self.catering_service.delete()


    
    


    