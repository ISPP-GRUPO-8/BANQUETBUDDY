from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import CateringService, Particular, Review, CustomUser, CateringCompany
from datetime import datetime

class CateringReviewTestCase(TestCase):
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

    def test_catering_review_view(self):
        self.client.login(username='testuser2', password='testpassword2')
        catering_id = self.catering_service.id

        description = 'Test review description'
        rating = 5

        url = reverse('add_review', kwargs={'catering_id': catering_id})
        response = self.client.post(url, {
            'description': description,
            'rating': rating,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(description = 'Test review description').exists())


    def test_catering_review_view_unauthenticated(self):
        response = self.client.get(reverse('add_review', kwargs={'catering_id': self.catering_service.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)


    def test_catering_review_view_invalid_rating(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_review', kwargs={'catering_id': self.catering_service.id}), {'description': 'Test review description', 'rating': 6})
        self.assertFalse(Review.objects.filter(description='Test review description').exists())
        

    def test_catering_review_view_invalid_catering_id(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.post(reverse('add_review', kwargs={'catering_id': 999}), {'description': 'Test review description', 'rating': 5})
        self.assertEqual(response.status_code, 404)
