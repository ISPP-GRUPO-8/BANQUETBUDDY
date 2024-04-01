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

class EmployeeOfferListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='12345',
            email='prueba@gmail.com'
            )
        
        self.catering_company = CateringCompany.objects.create(
            user=self.user, name='Test Catering Company',
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
        
    def test_employee_offer_list_view(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = self.user
        response = employee_offer_list(request)
        self.assertEqual(response.status_code, 200)
        
    def test_employee_offer_list_view_with_anonymous_user(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = AnonymousUser()
        response = employee_offer_list(request)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_employee_offer_list_view(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = self.user
        response = employee_offer_list(request)  # Cambio aquí
        self.assertEqual(response.status_code, 200)

    def test_employee_offer_list_view_with_anonymous_user(self):
        request = self.factory.get(reverse('employeeOfferList'))
        request.user = AnonymousUser()
        response = employee_offer_list(request)  # Cambio aquí
        self.assertEqual(response.status_code, 302)
        
    def tearDown(self) -> None:
        self.user.delete()
        self.catering_company.delete()
        self.catering_service.delete()
        self.offer.delete()
        
class ApplicationToOfferViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='12345'
            )
        
        self.employee = Employee.objects.create(
            user=self.user,
            phone_number='123456789',
            profession='Tester',
            experience='5 years',
            skills='Testing skills',
            english_level='ALTO',
            location='Test Location'
            )
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee.curriculum.save('curriculum.pdf', File(f))
        
        self.catering_company = CateringCompany.objects.create(
            user=self.user,
            name='Test Catering Company',
            address='Test Address',
            phone_number='987654321',
            cif='123456789A',
            is_verified=True,
            price_plan='Basic'
            )
        
        self.catering_service = CateringService.objects.create(
            cateringcompany=self.catering_company,
            name='Test Catering Service',
            description='Test Description',
            location='Test Location',
            capacity=100,
            price=100.00
            )
        self.offer = Offer.objects.create(
            cateringservice=self.catering_service,
            title='Test Offer',
            description='Test Description',
            requirements='Test Requirements',
            location='Test Location'
            )
        
    def test_application_to_offer_view_successful_application(self):
        request = self.factory.get(reverse('application_to_offer', args=[self.offer.id]))
        request.user = self.user
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
        request.user = self.user
        response = application_to_offer(request, self.offer.id)
        self.assertEqual(response.status_code, 200)  # Renders error template for already applied
        
    def test_application_to_offer_view_no_curriculum(self):
        self.employee.curriculum.delete()

        request = self.factory.get(reverse('application_to_offer', args=[self.offer.id]))
        request.user = self.user
        response = application_to_offer(request, self.offer.id)

        self.assertEqual(response.status_code, 200)
        
    def tearDown(self) -> None:
        self.user.delete()
        self.catering_company.delete()
        self.catering_service.delete()
        self.offer.delete()
        self.employee.delete()

class EmployeeApplicationsListTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.employee = Employee.objects.create(user=self.user, phone_number='123456789', profession='Developer', experience='2 years', skills='Python, Django', location='Somewhere')
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee.curriculum.save('curriculum.pdf', File(f))
                
        self.user_catering = CustomUser.objects.create_user(
            username='testuser2',
            password='12345',
            email='prueba@gmail.com'
            )
        
        self.catering_company = CateringCompany.objects.create(
            user=self.user_catering, name='Test Catering Company',
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

    def test_employee_applications_list_authenticated_employee(self):
        
        self.client.force_login(self.user)
        
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
        
    def tearDown(self) -> None:
        self.user.delete()
        self.employee.delete()
        
class TestNotifyEmployeeOnStateChange(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test_user', password='test_password')
        self.user_catering = CustomUser.objects.create_user(
            username='testuser2',
            password='12345',
            email='prueba@gmail.com'
            )
        
        self.catering_company = CateringCompany.objects.create(
            user=self.user_catering, name='Test Catering Company',
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
        self.employee = Employee.objects.create(user=self.user, phone_number='123456789', profession='Developer', experience='2 years', skills='Python, Django', location='Somewhere')
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee.curriculum.save('curriculum.pdf', File(f))
                
        self.job_application = JobApplication.objects.create(employee=self.employee, offer=self.offer, state='PENDING')
    
    def test_notify_employee_state(self):
        self.job_application.state = 'PENDING'
        self.job_application.save()
        notification = NotificationJobApplication.objects.filter(user=self.user, job_application=self.job_application).count()
        assert notification != 0

class EmployeeRecommendationLetterTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user1 = CustomUser.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')
        self.user2 = CustomUser.objects.create_user(username='testuser3', email='test3@example.com', password='testpassword3')
        self.user3 = CustomUser.objects.create_user(username='testuser4', email='test4@example.com', password='testpassword4')


        self.company = CateringCompany.objects.create (
            user=self.user,
            name='Test Catering Company',
            phone_number='123456789',
            service_description='Test service description',
            price_plan='BASE'
        )

        self.particular = Particular.objects.create(
            user=self.user1,
            phone_number='123456789',
            preferences='Test preferences',
            address='Test address',
            is_subscribed=False
        )

        self.employee = Employee.objects.create (
            user=self.user2,
            phone_number='123456789',
            profession='Tester',
            experience='5 years',
            skills='Testing skills',
            english_level='ALTO',
            location='Test Location'
        )
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee.curriculum.save('curriculum.pdf', File(f))

        self.employee2 = Employee.objects.create (
            user=self.user3,
            phone_number='123456789',
            profession='Tester',
            experience='5 years',
            skills='Testing skills',
            english_level='ALTO',
            location='Test Location'
        )
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee2.curriculum.save('curriculum.pdf', File(f))

        self.catering_service = CateringService.objects.create(
            cateringcompany=self.company,
            name='Test Catering Service',
            description='Test Description',
            location='Test Location',
            capacity=100, price=100.00
            )
        
        self.menu = Menu.objects.create(
            id = 1,
            cateringservice=self.catering_service,
            name='Test Menu',
            description='Test menu description',
            diet_restrictions='Test diet restrictions'
        )
        self.catering_service.menus.add(self.menu)

        self.event = Event.objects.create(
            cateringservice = self.catering_service,
            particular = self.particular,
            menu = self.menu,
            name = "Test Event",
            date = datetime.now().date(),
            details = "Test details",
            booking_state = BookingState.CONTRACT_PENDING,
            number_guests = 23
        )
        expiration_date = datetime.now().date() + timedelta(days=1)
        self.task = Task.objects.create(
            event=self.event,
            cateringservice=self.catering_service,
            cateringcompany=self.company,
            description='Test Task Description',
            assignment_date=datetime.now().date(),
            assignment_state='COMPLETED',
            expiration_date=expiration_date,
            priority='HIGH'
        )
        self.task.employees.add(self.employee)


        self.recommendation = RecommendationLetter.objects.create(
            employee = self.employee,
            catering = self.company,
            description = 'Test Recommendation Letter Description',
            date = datetime.now().date()
        )
    
    def test_my_recommendation_letters_view_authenticated(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_other_recommendation_letters_view(self):
        self.client.force_login(self.user3)
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 403)

    def test_no_employee_recommendation_letters_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 403)
    
    def test_my_recommendation_letters_view_unauthenticated(self):
        response = self.client.get(reverse('my_recommendation_letters', args=[self.employee.user.id]))
        self.assertEqual(response.status_code, 302)