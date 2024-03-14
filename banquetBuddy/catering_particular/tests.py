from django.test import TestCase, Client
from django.urls import reverse
from core.models import CustomUser, Particular, CateringCompany, CateringService
from .views import *
from catering_owners.models import CateringCompany, CateringService
from catering_particular.models import Particular
from core.models import CustomUser

class CateringViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear un usuario particular y datos asociados
        self.user_particular = CustomUser.objects.create_user(
            username="pablo@gmail.com", password="Pablo", email="pablo@gmail.com"
        )
        self.particular = Particular.objects.create(
            user=self.user_particular,
            phone_number="+123456789",
            preferences="Some preferences",
            address="Some address",
            is_subscribed=True,
        )

        # Crear un servicio de catering asociado al usuario particular
        self.catering_service = CateringService.objects.create(
            cateringcompany=CateringCompany.objects.create(
                user=self.user_particular,
                name="Catering Company 1",
                phone_number="+987654321",
                service_description="Some description",
                is_verified=True,
                price_plan="PREMIUM",
            ),
            name="Catering Service 1",
            description="Service description",
            location="Service location",
            capacity=100,
            price=1000.00,
        )

        # Autenticar al usuario particular
        self.client.login(username="pablo@gmail.com", password="Pablo")

    def test_listar_caterings_view(self):
        # Utiliza la ruta de listado de caterings
        url = reverse("listar_caterings")
        response = self.client.get(url)

        # Verificar que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que se utiliza el template correcto
        self.assertTemplateUsed(response, "listar_caterings.html")

        # Verificar que la respuesta contiene el nombre del servicio de catering
        self.assertContains(response, self.catering_service.name)

    def test_catering_detail_view(self):
        # Utiliza la ruta de detalle de catering con el ID correcto
        url = reverse(
            "catering_detail", kwargs={"catering_id": self.catering_service.id}
        )
        response = self.client.get(url)

        # Verificar que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que se utiliza el template correcto
        self.assertTemplateUsed(response, "catering_detail.html")

        # Verificar que la respuesta contiene el nombre del servicio de catering
        self.assertContains(response, self.catering_service.name)


class FiltrosTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear un usuario particular y datos asociados
        self.user_particular = CustomUser.objects.create_user(
            username="test", password="Test12345", email="test@gmail.com"
        )
        self.particular = Particular.objects.create(
            user=self.user_particular,
            phone_number="+123456789",
            preferences="Some preferences",
            address="Some address",
            is_subscribed=True,
        )
        # Autenticar al usuario particular
        self.client.login(username="test@gmail.com", password="Test12345")

    def test_filtrado_por_cocina(self):
        response = self.client.get(reverse("listar_caterings") + "?cocina=MEXICAN")
        self.assertEqual(response.status_code, 200)
        # Asegúrate de que solo los caterings de cocina mexicana están en la respuesta
        caterings = response.context["caterings"]
        for catering in caterings:
            self.assertTrue("MEXICAN" in catering.cateringcompany.cuisine_types)

    def test_filtrado_por_precio_maximo(self):
        response = self.client.get(reverse("listar_caterings") + "?precio_maximo=100")
        self.assertEqual(response.status_code, 200)
        # Asegúrate de que solo los caterings con precio menor o igual a 100 están en la respuesta
        caterings = response.context["caterings"]
        for catering in caterings:
            self.assertTrue(catering.price <= 100)

    def test_filtrado_por_num_invitados(self):
        response = self.client.get(reverse("listar_caterings") + "?num_invitados=50")
        self.assertEqual(response.status_code, 200)
        # Asegúrate de que solo los caterings con capacidad mayor o igual a 50 están en la respuesta
        caterings = response.context["caterings"]
        for catering in caterings:
            self.assertTrue(catering.capacity >= 50)

    # Asegúrate de que los filtros se limpian correctamente
    def test_limpiar_filtro_cocina(self):
        response = self.client.get(
            reverse("listar_caterings") + "?cocina=MEXICAN&limpiar_cocina=1"
        )
        self.assertEqual(response.status_code, 200)
        # Asegúrate de que no hay filtros de cocina en la respuesta
        self.assertFalse(response.context["cocina"])
