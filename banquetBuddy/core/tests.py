from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser
from catering_owners.models import CateringCompany, CateringService
from catering_particular.models import Particular
from django.test import TestCase, Client
from django.core import mail




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
        
class ResetPasswordTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_reset_password_view_get(self):
        response = self.client.get(reverse('reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reset_password.html')

    def test_reset_password_view_post_valid_email(self):
        response = self.client.post(reverse('reset_password'), {'email': 'test@example.com'})
        self.assertRedirects(response, reverse('reset_password'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset Password')

    def test_reset_password_view_post_invalid_email(self):
        response = self.client.post(reverse('reset_password'), {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reset_password.html')
        self.assertNotEqual(len(mail.outbox), 1)

    def tearDown(self):
        self.user.delete()

class ResetPasswordConfirmTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user.generate_reset_password_token()

    def test_reset_password_confirm_view_get(self):
        response = self.client.get(reverse('reset_password_confirm', kwargs={'token': self.user.reset_password_token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reset_password_confirm.html')

    def test_reset_password_confirm_view_post_valid_token(self):
        response = self.client.post(reverse('reset_password_confirm', kwargs={'token': self.user.reset_password_token}),
                                    {'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_reset_password_confirm_view_post_invalid_token(self):
        response = self.client.post(reverse('reset_password_confirm', kwargs={'token': 'invalidtoken'}),
                                    {'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reset_password'))
        self.assertTrue(self.client.session.get('_auth_user_id') is None)

    def tearDown(self):
        self.user.delete()

class ResetPasswordTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_reset_password_view_get(self):
        response = self.client.get(reverse('reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reset_password.html')

    def test_reset_password_view_post_valid_email(self):
        response = self.client.post(reverse('reset_password'), {'email': 'test@example.com'})
        self.assertRedirects(response, reverse('reset_password'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reset Password')

    def test_reset_password_view_post_invalid_email(self):
        response = self.client.post(reverse('reset_password'), {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reset_password.html')
        self.assertNotEqual(len(mail.outbox), 1)

    def tearDown(self):
        self.user.delete()

class ResetPasswordConfirmTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user.generate_reset_password_token()

    def test_reset_password_confirm_view_get(self):
        response = self.client.get(reverse('reset_password_confirm', kwargs={'token': self.user.reset_password_token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reset_password_confirm.html')

    def test_reset_password_confirm_view_post_valid_token(self):
        response = self.client.post(reverse('reset_password_confirm', kwargs={'token': self.user.reset_password_token}),
                                    {'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_reset_password_confirm_view_post_invalid_token(self):
        response = self.client.post(reverse('reset_password_confirm', kwargs={'token': 'invalidtoken'}),
                                    {'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reset_password'))
        self.assertTrue(self.client.session.get('_auth_user_id') is None)

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


    
    


    