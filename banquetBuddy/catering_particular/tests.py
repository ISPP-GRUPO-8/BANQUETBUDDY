from django.test import TestCase, Client
from django.urls import reverse
from core.models import CateringService, CustomUser, Particular, CateringCompany

class CateringViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_particular = CustomUser.objects.create(username='particular_user', email='particular@example.com')
        self.particular = Particular.objects.create(user=self.user_particular, phone_number='+123456789', preferences='Some preferences', address='Some address', is_subscribed=True)
        self.user_catering_company = CustomUser.objects.create(username='catering_company_user', email='catering@example.com')
        self.catering_company = CateringCompany.objects.create(user=self.user_catering_company, name='Catering Company', phone_number='+987654321', service_description='Some service description', is_verified=True, price_plan='BASE')
        self.catering_service = CateringService.objects.create(cateringcompany=self.catering_company, name='Catering 1', description='Description 1', location='Location 1', capacity=100, price=100.00)

    def test_listar_caterings_view(self):
        url = reverse('listar_caterings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listar_caterings.html')
        self.assertContains(response, self.catering_service.name)

    def test_catering_detail_view(self):
        url = reverse('catering_detail', kwargs={'catering_id': self.catering_service.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catering_detail.html')
        self.assertContains(response, self.catering_service.name)
