from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from .models import Employee
from core.models import CustomUser
from catering_owners.models import Offer, JobApplication, CateringService, CateringCompany, CateringService, Menu, Event, BookingState, CateringCompany, Particular
from .views import employee_offer_list, application_to_offer
from django.urls import reverse

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

class BookingProcessTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user1 = CustomUser.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')

        self.company = CateringCompany.objects.create(
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

        self.catering_service = CateringService.objects.create(
            cateringcompany=self.company,
            name='Test Catering Service',
            description='Test service description',
            location='Test location',
            capacity=100,
            price=100.00
        )

        self.menu = Menu.objects.create(
            cateringservice=self.catering_service,
            name='Test Menu',
            description='Test menu description',
            price=50.00,
            diet_restrictions='Test diet restrictions'
        )
        self.catering_service.menus.add(self.menu)

        self.client = Client()

    def test_booking_process(self):
        self.client.login(username='testuser2', password='testpassword2')
        catering_id = self.catering_service.id
        url = reverse('booking_process', kwargs={'catering_id': catering_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {'event_date': '2024-03-11', 'number_guests': '50', 'menu_selected': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(cateringservice=self.catering_service, date='2024-03-11', number_guests=50).exists())

    def test_invalid_booking_process(self):
        self.client.login(username='testuser2', password='testpassword2')
        catering_id = self.catering_service.id
        url = reverse('booking_process', kwargs={'catering_id': catering_id})

        response = self.client.post(url, {'event_date': '2024-03-11', 'number_guests': '1000', 'menu_selected': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(cateringservice=self.catering_service).exists())

        response = self.client.post(url, {'event_date': '2024-03-11', 'number_guests': '10', 'menu_selected': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(cateringservice=self.catering_service).exists())

        response = self.client.post(url, {'event_date': '2020-03-11', 'number_guests': '10', 'menu_selected': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(cateringservice=self.catering_service).exists())

    def test_unauthorized_access(self):
        catering_id = self.catering_service.id
        url = reverse('booking_process', kwargs={'catering_id': catering_id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
