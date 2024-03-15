from django.test import TestCase, Client
from django.urls import reverse
from core.models import CustomUser, BookingState
from datetime import datetime, timedelta
from core.models import CustomUser
from catering_owners.models import CateringCompany, CateringService, Menu, Event
from .views import *
from catering_particular.models import Particular

class BookTestCase(TestCase):
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
            id = 1,
            cateringservice=self.catering_service,
            name='Test Menu',
            description='Test menu description',
            diet_restrictions='Test diet restrictions'
        )
        self.catering_service.menus.add(self.menu)
        
        self.menu2 = Menu.objects.create(
            id = 2,
            cateringservice=self.catering_service,
            name='Test Menu 2',
            description='Test menu description 2',
            diet_restrictions='Test diet restrictions 2'
        )
        self.catering_service.menus.add(self.menu2)

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
    
        self.client = Client()

    def test_my_books_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('my_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_books.html')
    
    def test_my_books_view_not_authorized(self):
        response = self.client.get(reverse('my_books'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_book_edit_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('book_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_edit.html')

        response = self.client.post(reverse('book_edit', args=[self.event.id]), {
            'date': '2024-04-15',
            'number_guests': '10',
            'selected_menu': self.menu2.id, 
        })
        self.assertEqual(response.status_code, 200)
        edited_event = Event.objects.get(id=self.event.id)
        self.assertEqual(edited_event.date.strftime('%Y-%m-%d'), '2024-04-15')
        self.assertEqual(edited_event.number_guests, 10)
        self.assertEqual(edited_event.menu, self.menu2)
        self.assertEqual(edited_event.booking_state, BookingState.CONTRACT_PENDING)
    
    def test_book_edit_view_incomplete_form(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('book_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_edit.html')

        response = self.client.post(reverse('book_edit', args=[self.event.id]), {
            'date': '2024-03-15',
            'number_guests': '0',
            'selected_menu': self.menu2.id,
        })
        self.assertEqual(response.status_code, 200)

        edited_event = Event.objects.get(id=self.event.id)
        self.assertEqual(edited_event.date, self.event.date) 
        self.assertEqual(edited_event.number_guests, self.event.number_guests)  
        self.assertEqual(edited_event.menu, self.event.menu) 
        self.assertEqual(edited_event.booking_state, self.event.booking_state)  

    def test_book_edit_view_past_date(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('book_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_edit.html')

        past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.post(reverse('book_edit', args=[self.event.id]), {
            'date': past_date,
            'number_guests': '10',
            'selected_menu': self.menu2.id,
        })
        
        self.assertEqual(response.status_code, 200)

        edited_event = Event.objects.get(id=self.event.id)
        self.assertEqual(edited_event.date, self.event.date) 
        self.assertEqual(edited_event.number_guests, self.event.number_guests)  
        self.assertEqual(edited_event.menu, self.event.menu) 
        self.assertEqual(edited_event.booking_state, self.event.booking_state)

    
    def test_book_cancel_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('book_cancel', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        canceled_event = Event.objects.get(id=self.event.id)
        self.assertEqual(canceled_event.booking_state, BookingState.CANCELLED)

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
