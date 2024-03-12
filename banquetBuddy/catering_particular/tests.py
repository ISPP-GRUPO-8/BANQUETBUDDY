from django.test import TestCase, Client
from django.urls import reverse
from catering_owners.models import CateringCompany, CateringService
from catering_particular.models import Particular

from core.models import CustomUser

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
