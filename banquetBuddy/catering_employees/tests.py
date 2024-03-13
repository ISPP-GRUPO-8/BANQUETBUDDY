from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import CateringService, Menu, Event, BookingState, CustomUser, CateringCompany, Particular
from datetime import datetime
from django.urls import reverse


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
