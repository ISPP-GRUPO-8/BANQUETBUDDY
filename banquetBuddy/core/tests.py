from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from catering_employees.models import Employee
from .models import CustomUser
from catering_owners.models import CateringCompany

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