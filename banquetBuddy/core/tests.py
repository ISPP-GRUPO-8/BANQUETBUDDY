from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from catering_employees.models import Employee
from .models import CustomUser
from catering_owners.models import CateringCompany, CateringService
from catering_particular.models import Particular

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
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    # Tests the login with valid credentials
    def test_login_view_valid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'test@example.com', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))
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

        self.assertRedirects(response, reverse('home'))

    def tearDown(self):
        self.user.delete()
        
class ErrorReportTestCase(TestCase):
    def setUp(self):
        # Particular
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_error_report_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('error-report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/error_report.html')

    def test_error_report_view_get_without_login(self):
        response = self.client.get(reverse('error-report'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login?next=/error-report')  

    def test_error_report_view_post_particular(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'name': 'John',
            'surname': 'Doe',
            'message': 'Test error message',
            'error_type': 'bug',
            'reporter_email': 'test@example.com',
        }
        response = self.client.post(reverse('error-report'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')  

    def test_error_report_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        data = {}
        response = self.client.post(reverse('error-report'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'surname', 'This field is required.')
        self.assertFormError(response, 'form', 'message', 'This field is required.')
        self.assertFormError(response, 'form', 'error_type', 'This field is required.')
        self.assertFormError(response, 'form', 'reporter_email', 'This field is required.')

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
