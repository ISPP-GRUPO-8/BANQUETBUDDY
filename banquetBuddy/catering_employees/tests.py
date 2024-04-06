from asyncio import Task
import os
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse

from .models import Employee
from catering_particular.models import Particular
from core.models import CustomUser
from catering_owners.models import *
from .views import employee_offer_list, application_to_offer
from django.urls import reverse
from datetime import datetime, timedelta, date
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from .signals import notify_employee_on_state_change
from django.core.files import File

# Create your tests here.



class EmployeeTestCases(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_employee1 = CustomUser.objects.create_user(
            username='testuser_employee1',
            password='12345',
            email='employee@gmail.com'
            )
        
        self.user_employee2 = CustomUser.objects.create_user(
            username='testuser_employee2',
            email='employee2@example.com',
            password='testpassword4'
            )
        
        self.user_catering_company = CustomUser.objects.create_user(
            username='testuser_catering_company',
            password='12345',
            email='cateringCompany@gmail.com'
            )
        
        self.employee = Employee.objects.create(
            user=self.user_employee1,
            phone_number='123456789',
            profession='Tester',
            experience='5 years',
            skills='Testing skills',
            english_level='ALTO',
            location='Test Location'
            )
        
        self.employee2 = Employee.objects.create (
            user=self.user_employee2,
            phone_number='123456789',
            profession='Tester',
            experience='5 years',
            skills='Testing skills',
            english_level='ALTO',
            location='Test Location'
        )
        
        self.catering_company = CateringCompany.objects.create(
            user=self.user_catering_company, name='Test Catering Company',
            address='Test Address', phone_number='987654321',
            cif='123456789A', is_verified=True,
            price_plan='Basic'
            )
        
        self.catering_service = CateringService.objects.create(
            cateringcompany=self.catering_company,
            name='Test Catering Service',
            description='Test Description',
            location='Test Location',
            capacity=100, price=100.00
            )
        
        self.offer = Offer.objects.create(
            cateringservice=self.catering_service ,
            title='Test Offer',
            description='Test Description',
            requirements='Test Requirements',
            location='Test Location'
            )
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee.curriculum.save('curriculum.pdf', File(f))
        
    def create_specific_job_application(self):
        
        self.job_application = JobApplication.objects.create(
            employee=self.employee,
            offer=self.offer,
            state='PENDING'
            )

    # Test para la vista de lista de ofertas de empleo
    def test_employee_offer_list_view(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = self.user_employee1
        response = employee_offer_list(request)
        self.assertEqual(response.status_code, 200)
        
    def test_employee_offer_list_view_with_anonymous_user(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = AnonymousUser()
        response = employee_offer_list(request)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_employee_offer_list_view(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = self.user_employee1
        response = employee_offer_list(request)  # Cambio aquí
        self.assertEqual(response.status_code, 200)

    def test_employee_offer_list_view_with_anonymous_user(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = AnonymousUser()
        response = employee_offer_list(request)  # Cambio aquí
        self.assertEqual(response.status_code, 302)

    # Test para la vista de solicitud de empleo
    def test_application_to_offer_view_successful_application(self):
        request = self.factory.get(reverse('application_to_offer', args=[self.offer.id]))
        request.user = self.user_employee1
        response = application_to_offer(request, self.offer.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(JobApplication.objects.filter(employee=self.employee, offer=self.offer).exists())
        
    def test_application_to_offer_view_invalid_employee(self):
        
        invalid_user = CustomUser.objects.create_user(
            username='invaliduser',
            password='12345',
            email='prueba@gmail.com'
            )
        
        request = self.factory.get(reverse('application_to_offer', args=[self.offer.id]))
        request.user = invalid_user
        response = application_to_offer(request, self.offer.id)
        self.assertEqual(response.status_code, 200)  # Renders error template for invalid employee
        
    def test_application_to_offer_view_already_applied(self):
        JobApplication.objects.create(employee=self.employee, offer=self.offer, state='PENDING')
        request = self.factory.get(reverse('application_to_offer', args=[self.offer.id]))
        request.user = self.user_employee1
        response = application_to_offer(request, self.offer.id)
        self.assertEqual(response.status_code, 200)  # Renders error template for already applied
        
    def test_application_to_offer_view_no_curriculum(self):
        self.employee.curriculum.delete()

        request = self.factory.get(reverse('application_to_offer', args=[self.offer.id]))
        request.user = self.user_employee1
        response = application_to_offer(request, self.offer.id)

        self.assertEqual(response.status_code, 200)

    # Test para la vista de lista de aplicaciones de empleo
    def test_employee_applications_list_authenticated_employee(self):
        
        self.client.force_login(self.user_employee1)
        
        job_application = JobApplication.objects.create(employee=self.employee, offer=self.offer, date_application=date.today())
        
        # Hacemos una solicitud GET a la vista
        response = self.client.get(reverse('JobApplicationList'))
        
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(job_application, response.context['applications'])

    def test_employee_applications_list_authenticated_non_employee(self):

        non_employee_user = CustomUser.objects.create_user(username='nonemployee', email='nonemployee@example.com', password='password')
        # Simulamos que el usuario está autenticado
        self.client.force_login(non_employee_user)
        
        # Hacemos una solicitud GET a la vista
        response = self.client.get(reverse('JobApplicationList'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error_employee.html')

    def test_employee_applications_list_unauthenticated(self):
        # Simulamos que el usuario no está autenticado
        self.client.logout()
        
        response = self.client.get(reverse('JobApplicationList'))
        
        # Verificamos que la respuesta sea 302 Redireccionamiento
        self.assertEqual(response.status_code, 302)
    
    # Test para la vista de notificación de aplicación de empleo
    def test_notify_employee_state(self):
        self.create_specific_job_application()
        self.job_application.state = 'PENDING'
        self.job_application.save()
        notification = NotificationJobApplication.objects.filter(user=self.user_employee1, job_application=self.job_application).count()
        assert notification != 0
    
    # Test para la vista de recommendation letters
    def test_my_recommendation_letters_view_authenticated(self):
        self.client.force_login(self.user_employee1)
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_other_recommendation_letters_view(self):
        self.client.force_login(self.user_employee2)
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 403)

    def test_no_employee_recommendation_letters_view(self):
        self.client.force_login(self.user_catering_company)
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 403)
    
    def test_my_recommendation_letters_view_unauthenticated(self):
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 302)