from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from .models import Employee
from core.models import CustomUser
from catering_owners.models import Offer, JobApplication, CateringService, CateringCompany, CateringService, Menu, Event, BookingState, CateringCompany, NotificationJobApplication
from .views import employee_offer_list, application_to_offer
from django.urls import reverse
from datetime import date
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from .signals import notify_employee_on_state_change

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
        file_content = b'Contenido de prueba del archivo'
        false_file = ContentFile(file_content, name='archivo_prueba.txt')
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
            location='Test Location',
            curriculum=false_file
            )
        
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
        self.job_application = JobApplication.objects.create(employee=self.employee, offer=self.offer, state='PENDING')
    
    def test_notify_employee_state(self):
        self.job_application.state = 'PENDING'
        self.job_application.save()
        notification = NotificationJobApplication.objects.filter(user=self.user, job_application=self.job_application).count()
        assert notification is not 0