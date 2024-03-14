from django.test import TestCase, Client
from django.urls import reverse
from core.models import CustomUser, Particular, CateringCompany, CateringService, Review

class CateringViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear un usuario particular y datos asociados
        self.user_particular = CustomUser.objects.create_user(username='pablo@gmail.com', password='Pablo', email='pablo@gmail.com')
        self.particular = Particular.objects.create(user=self.user_particular, phone_number='+123456789', preferences='Some preferences', address='Some address', is_subscribed=True)

        # Crear un servicio de catering asociado al usuario particular
        self.catering_service = CateringService.objects.create(
            cateringcompany=CateringCompany.objects.create(
                user=self.user_particular,
                name='Catering Company 1',
                phone_number='+987654321',
                service_description='Some description',
                is_verified=True,
                price_plan='PREMIUM'
            ),
            name='Catering Service 1',
            description='Service description',
            location='Service location',
            capacity=100,
            price=1000.00
        )

        # Autenticar al usuario particular
        self.client.login(username='pablo@gmail.com', password='Pablo')

    def test_listar_caterings_view(self):
        # Utiliza la ruta de listado de caterings
        url = reverse('listar_caterings')
        response = self.client.get(url)

        # Verificar que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que se utiliza el template correcto
        self.assertTemplateUsed(response, 'listar_caterings.html')

        # Verificar que la respuesta contiene el nombre del servicio de catering
        self.assertContains(response, self.catering_service.name)

    def test_catering_detail_view(self):
        # Utiliza la ruta de detalle de catering con el ID correcto
        url = reverse('catering_detail', kwargs={'catering_id': self.catering_service.id})
        response = self.client.get(url)

        # Verificar que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que se utiliza el template correcto
        self.assertTemplateUsed(response, 'catering_detail.html')

        # Verificar que la respuesta contiene el nombre del servicio de catering
        self.assertContains(response, self.catering_service.name)

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

