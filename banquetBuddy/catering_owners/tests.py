from decimal import Decimal
import os
from django.test import Client, LiveServerTestCase, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from catering_particular.models import Particular
from catering_employees.forms import EmployeeFilterForm
from catering_employees.models import Employee
from catering_owners.models import *
from .views import *
from catering_particular.models import Particular
from core.forms import CustomUserCreationForm
from .forms import CateringCompanyForm
from core.models import CustomUser, BookingState
from phonenumbers import parse
from datetime import datetime, timedelta
from django.core.files import File
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
import time



class CateringBookTestCase(TestCase):
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
            cateringcompany = self.company,
            menu = self.menu,
            name = "Test Event",
            date = datetime.now().date(),
            details = "Test details",
            booking_state = BookingState.CONTRACT_PENDING,
            number_guests = 23
        )
    
        self.client = Client()

    def test_my_books_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'particular_books.html')
    
    def test_my_books_view_not_authorized(self):
        response = self.client.get(reverse('catering_books'))
        self.assertEqual(response.status_code, 302)

    def test_book_edit_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_books_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catering_book_edit.html')

        response = self.client.post(reverse('catering_books_edit', args=[self.event.id]), {
            'date': '2024-04-15',
            'number_guests': '10',
            'selected_menu': self.menu2.id, 
        })
        self.assertEqual(response.status_code, 302)
        edited_event = Event.objects.get(id=self.event.id)
        self.assertEqual(edited_event.date.strftime('%Y-%m-%d'), '2024-04-15')
        self.assertEqual(edited_event.number_guests, 10)
        self.assertEqual(edited_event.menu, self.menu2)
        self.assertEqual(edited_event.booking_state, BookingState.CONTRACT_PENDING)
    
    def test_book_edit_view_incomplete_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_books_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catering_book_edit.html')

        response = self.client.post(reverse('catering_books_edit', args=[self.event.id]), {
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
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_books_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catering_book_edit.html')

        past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.post(reverse('catering_books_edit', args=[self.event.id]), {
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
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_books_cancel', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        canceled_event = Event.objects.get(id=self.event.id)
        self.assertEqual(canceled_event.booking_state, BookingState.CANCELLED)

class RegisterCompanyTestCase(TestCase):
    def test_register_company_view(self):
        response = self.client.get(reverse('register_company'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro_company.html')

    # def test_register_company_post(self):
    #     # Construye la ruta al archivo PDF de prueba dentro del proyecto
    #     file_name = "test_pdf.pdf"
    #     file_path = os.path.join(os.path.dirname(__file__), 'test_files', file_name)

    #     # Lee el contenido del archivo PDF
    #     with open(file_path, "rb") as file:
    #         file_content = file.read()

    #     # Crea el objeto SimpleUploadedFile con el contenido del archivo PDF
    #     file_mock = SimpleUploadedFile(file_name, file_content, content_type='application/pdf')

        
    #     data = {
    #         'username': 'user_cool',
    #         "first_name": "Test",
    #         "last_name": "User",
    #         "email":"emailtest@gmail.com",
    #         'password1': 'easy_password',
    #         'password2': 'easy_password',
    #         'name': 'Test Company',
    #         'address': 'Test Address',
    #         'phone_number': '+34666555444',
    #         'cif': 'A1234567J',
    #         'price_plan': 'BASE',
    #     }
    #     files = {'verification_document': file_mock}

        
    #     response = self.client.post(reverse('register_company'), data, files=files, follow=True)

    #     # Verificar que la respuesta sea correcta. NO LO ES, MUESTA CODIGO 200
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('home'))
    #     self.assertContains(response, "Registration successful!")
    #     form = response.context.get('form')
    #     if form:
    #         print(form.errors)


    
    def test_catering_company_form(self):
        # Construye la ruta al archivo PDF de prueba dentro del proyecto
        file_name = "test_pdf.pdf"
        file_path = os.path.join(os.path.dirname(__file__), 'test_files', file_name)

        # Lee el contenido del archivo PDF
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Crea el objeto SimpleUploadedFile con el contenido del archivo PDF
        file_mock = SimpleUploadedFile(file_name, file_content, content_type='application/pdf')

        
        user_data = {
            'username': 'user_cool',
            "first_name": "Test",
            "last_name": "User",
            "email":"emailtest@gmail.com",
            'password1': 'easy_password',
            'password2': 'easy_password',
        }

        user_form = CustomUserCreationForm(data=user_data)
        print(user_form.errors)
        self.assertTrue(user_form.is_valid())
        user = user_form.save()

        form_data = {
            'username': 'user_cool',
            "first_name": "Test",
            "last_name": "User",
            "email":"emailtest@gmail.com",
            'password1': 'easy_password',
            'password2': 'easy_password',
            'name': 'Test Company',
            'address': 'Test Address',
            'phone_number': '+34666555444',
            'cif': 'A1234567J',
            'price_plan': 'BASE',
        }
        files = {'verification_document': file_mock}

        form = CateringCompanyForm(data=form_data, files=files)

        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    
    def setUp(self) -> None:
        
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='testuser@gmail.com')
        self.user_particular = CustomUser.objects.create_user(username='testuser2', password='testpassword', email='testuser2@gmail.com')
        phone_number = parse("+15551234567", "US")
        self.catering_company = CateringCompany.objects.create(user=self.user, name='Prueba', phone_number=str(phone_number), service_description='Prueba', price_plan='PREMIUM_PRO')
        self.particular = Particular.objects.create(user=self.user_particular)
        self.catering_service = CateringService.objects.create(
            cateringcompany=self.catering_company,
            name="Brunch para la oficina",
            description="Delicioso brunch con variedad de opciones dulces y saladas perfecto para reuniones de trabajo.",
            location="Calle Mayor, 123",
            capacity=50,
            price=Decimal("129.99"),
        )
        self.menu = Menu.objects.create(
            id = 1,
            cateringservice=self.catering_service,
            name='Test Menu',
            description='Test menu description',
            diet_restrictions='Test diet restrictions'
        )
        self.event = Event.objects.create(
            cateringservice = self.catering_service,
            particular = self.particular,
            cateringcompany = self.catering_company,
            menu = self.menu,
            name = "Test Event",
            date = datetime.now().date(),
            details = "Test details",
            booking_state = BookingState.CONTRACT_PENDING,
            number_guests = 23
        )
        self.offer = Offer.objects.create(title="Oferta de prueba", event=self.event, description="Descripción de prueba", requirements="Requisitos de prueba", location="Ubicación de prueba",cateringservice= self.catering_service, start_date = datetime.now().date(), end_date=datetime.now().date() + timedelta(days=1))
        self.employee = Employee.objects.create(user=CustomUser.objects.create(username="usuario_prueba", email= 'estoesunaprueba@gmail.com'), phone_number="1234567890", profession="Chef", experience="5 years", skills="Culinary skills", english_level="C2", location="Ubicación de prueba")
        
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', 'curriculum.pdf')
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                self.employee.curriculum.save('curriculum.pdf', File(f))
                
        self.job_application = JobApplication.objects.create(employee=self.employee, offer=self.offer, date_application="2023-11-14", state="APLICADO")

    def test_get_applicants(self):
        
        self.client.force_login(self.user)

        # Simula una solicitud HTTP a la vista
        response = self.client.get(f"/applicants/{self.offer.id}/")

        # Comprueba el código de respuesta HTTP
        self.assertEqual(response.status_code, 200)

        # Comprueba que la plantilla correcta se ha renderizado
        self.assertTemplateUsed(response, "applicants_list.html")

        # Comprueba que la lista de solicitantes contiene el empleado de prueba
        applicants = response.context['applicants']
        self.assertEqual(len(applicants), 1)
        self.assertEqual(applicants[0].employee.user.username, "usuario_prueba")
        
    def test_employee_filter_form(self):
        # Crea datos para el formulario de filtro
        data = {
            'english_level': 'C2',
            'profession': 'Chef',
            'experience': '5 years',
            'skills': 'Culinary skills',
        }

        # Crea una instancia del formulario de filtro con los datos
        form = EmployeeFilterForm(data)

        # Verifica que el formulario sea válido
        self.assertTrue(form.is_valid())

        # Obtén el queryset original de la vista
        original_queryset = self.offer.job_applications.select_related('employee').all()

        # Filtra el queryset con el formulario
        filtered_queryset = form.filter_queryset(original_queryset)

        # Verifica que el queryset filtrado tenga el tamaño esperado (1 en este caso)
        self.assertEqual(filtered_queryset.count(), 1)


    def test_profile_edit_view_get(self):
        # Prueba GET request a la vista
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_company_edit.html')
        
    def tearDown(self) -> None:
        self.user.delete()
        self.catering_company.delete()
        self.catering_service.delete()
        self.offer.delete()
        self.employee.delete()
        self.job_application.delete()


class CateringViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = CustomUser.objects.create_user(username='test_user', password='test_password',email='testuser@gmail.com')
        self.user2 = CustomUser.objects.create_user(username='test_user2', password='test_password2')
        
        self.catering_company = CateringCompany.objects.create(user=self.user, name='Test Catering Company',price_plan = "PREMIUM_PRO")
        self.catering_company2 = CateringCompany.objects.create(
            user=self.user2,
            name='Catering Company 2',
            price_plan = "PREMIUM"
        )
        self.catering_service = CateringService.objects.create(
            name='Test Catering',
            cateringcompany=self.catering_company,
            description='Test description',
            location='Test location',
            capacity=100,
            price=500.00
        )
        self.particular = Particular.objects.create(user=self.user)
        self.menu = Menu.objects.create(name='Test Menu')
        self.event_date = datetime.now().date()
        self.event = Event.objects.create(
            cateringservice=self.catering_service,
            particular=self.particular,
            cateringcompany = self.catering_company,
            menu=self.menu,
            name='Test Event',
            date=self.event_date,
            details='Test details',
            booking_state=BookingState.choices[0][0],
            number_guests=10
        )

    def test_view_reservations_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('view_reservations', kwargs={'catering_service_id': self.catering_service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')

    def test_view_reservation_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('view_reservation', kwargs={'catering_service_id': self.catering_service.pk, 'event_id': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_reservation.html')

    def test_catering_calendar_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('catering_calendar', kwargs={'catering_service_id': self.catering_service.pk, 'year': self.event_date.year, 'month': self.event_date.month}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar.html')

    def test_reservations_for_day_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('reservations_for_day', kwargs={'catering_service_id': self.catering_service.pk, 'year': self.event_date.year, 'month': self.event_date.month, 'day': self.event_date.day}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations_for_day.html')

    def test_next_month_view_authenticated(self):
        # Prueba para avanzar al mes siguiente en el calendario cuando el usuario está autenticado
        self.client.force_login(self.user)
        response = self.client.get(reverse('next_month', kwargs={'catering_service_id': self.catering_service.pk, 'year': self.event_date.year, 'month': self.event_date.month}))
        self.assertEqual(response.status_code, 302)
        next_month_date = self.event_date.replace(day=1) + timedelta(days=32)  # Obtener la fecha del mes siguiente
        self.assertRedirects(response, reverse('catering_calendar', kwargs={'catering_service_id': self.catering_service.pk, 'year': next_month_date.year, 'month': next_month_date.month}))

    def test_prev_month_view_authenticated(self):
        # Prueba para retroceder al mes anterior en el calendario cuando el usuario está autenticado
        self.client.force_login(self.user)
        response = self.client.get(reverse('prev_month', kwargs={'catering_service_id': self.catering_service.pk, 'year': self.event_date.year, 'month': self.event_date.month}))
        self.assertEqual(response.status_code, 302)
        prev_month_date = self.event_date.replace(day=1) - timedelta(days=1)  # Obtener la fecha del mes anterior
        self.assertRedirects(response, reverse('catering_calendar', kwargs={'catering_service_id': self.catering_service.pk, 'year': prev_month_date.year, 'month': prev_month_date.month}))

    def test_permission_denied(self):
        # Intentar acceder a las vistas protegidas sin iniciar sesión
        self.client.force_login(self.user2)
        response_view_reservations = self.client.get(reverse('view_reservations', kwargs={'catering_service_id': self.catering_service.pk}))
        response_view_reservation = self.client.get(reverse('view_reservation', kwargs={'catering_service_id': self.catering_service.pk, 'event_id': self.event.pk}))
        response_catering_calendar = self.client.get(reverse('catering_calendar', kwargs={'catering_service_id': self.catering_service.pk, 'year': self.event_date.year, 'month': self.event_date.month}))
        response_reservations_for_day = self.client.get(reverse('reservations_for_day', kwargs={'catering_service_id': self.catering_service.pk, 'year': self.event_date.year, 'month': self.event_date.month, 'day': self.event_date.day}))

        # Verificar si se devuelve un error de permiso
        self.assertEqual(response_view_reservations.status_code, 403)
        self.assertEqual(response_view_reservation.status_code, 403)
        self.assertEqual(response_catering_calendar.status_code, 403)
        self.assertEqual(response_reservations_for_day.status_code, 403)

class RecommendationLetterTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user1 = CustomUser.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')
        self.user2 = CustomUser.objects.create_user(username='testuser3', email='test3@example.com', password='testpassword3')


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
            cateringcompany = self.company,
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

    def test_list_employee_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('list_employee', args=[self.catering_service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_employee.html')

    def test_recommendation_letter_creation_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('recommendation_letter', args=[self.catering_service.id, self.employee.user.id]), {
            'description': 'Description',
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(RecommendationLetter.objects.filter(employee=self.employee).exists())

    def test_recommendation_letter_creation_unauthenticated(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('recommendation_letter', args=[self.catering_service.id, self.employee.user.id]))
        self.assertEqual(response.status_code, 403)

    def test_recommendation_letter_get_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recommendation_letter', args=[self.catering_service.id, self.employee.user.id]))
        self.assertEqual(response.status_code, 200)  

class ChatViewTestCase(TestCase):
    def setUp(self):
        # Crear usuarios personalizados
        self.particular_user = CustomUser.objects.create_user(username='particular_user', email='particular@example.com', password='password')
        self.employee_user = CustomUser.objects.create_user(username='employee_user', email='employee@example.com', password='password')
        self.company_user = CustomUser.objects.create_user(username='company_user', email='company@example.com', password='password')

        # Crear instancias de Particular, Employee y CateringCompany
        self.particular = Particular.objects.create(user=self.particular_user)
        self.employee = Employee.objects.create(user=self.employee_user)
        self.company = CateringCompany.objects.create(user=self.company_user)

        # Crear algunos mensajes
        Message.objects.create(sender=self.particular_user, receiver=self.company_user, date=timezone.now(), content="Hola desde el particular")
        Message.objects.create(sender=self.company_user, receiver=self.particular_user, date=timezone.now(), content="Hola desde la empresa")

    def test_chat_view_particular(self):
        # Prueba la vista de chat para un usuario particular
        self.client.force_login(self.particular_user)
        response = self.client.get('/chat/{}/'.format(self.company.user.id))
        self.assertEqual(response.status_code, 200)

    def test_chat_view_employee(self):
        # Prueba la vista de chat para un empleado
        self.client.force_login(self.employee_user)
        response = self.client.get('/chat/{}/'.format(self.company.user.id))
        self.assertEqual(response.status_code, 200)

    def test_chat_view_catering_company(self):
        # Prueba la vista de chat para una empresa de catering
        self.client.force_login(self.company_user)
        response = self.client.get('/chat/{}/'.format(self.particular.user.id))
        self.assertEqual(response.status_code, 200)

class CateringViewTest(TestCase):
    def setUp(self):
        # Configurar el entorno de prueba con objetos necesarios
        self.client = Client()

        self.user = CustomUser.objects.create_user(username='test_user', password='test_password',email='testuser@gmail.com')
        self.user1 = CustomUser.objects.create_user(username='test_user1', password='test_password1',email='testuser1@gmail.com')

        self.catering_company = CateringCompany.objects.create(user=self.user, name='Test Catering Company',price_plan = "PREMIUM_PRO")
        
        self.message = Message.objects.create(
            sender=self.user,
            receiver=self.user1,
            date=datetime.now(),
            content="Este es un mensaje de ejemplo."
        )

    def test_listar_caterings_particular(self):
        # Simular una solicitud HTTP al punto final
        self.client.force_login(self.user)


        # Realizar la solicitud HTTP
        response = self.client.get(reverse('listar_caterings_particular'))

        # Verificar si la respuesta es exitosa
        self.assertEqual(response.status_code, 200)

        # Verificar si el template utilizado es el esperado
        self.assertTemplateUsed(response, 'contact_chat_owner.html')
        
        # Verificar si el contexto se pasa correctamente al template
        self.assertTrue(response.context['is_catering_company'])
        
        self.assertIn('messages', response.context)
        
        
    def test_listar_caterings_particular_unauthenticated(self):
        # Realizamos una solicitud GET a la vista sin autenticar al usuario
        response = self.client.get(reverse('listar_caterings_particular'))

        # Verificamos que el usuario no autenticado reciba un código de estado 302 para redirigirlo 
        self.assertEqual(response.status_code, 302)



########################
###Tests de interfaz####
########################

class RegisterFormTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path=settings.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)  # Espera implícita de hasta 10 segundos

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_register_form(self):
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'test_files', 'test_pdf.pdf')
        self.selenium.get(self.live_server_url + '/register_choice')  # URL de la vista para elegir el tipo de registro

        # Simula la interacción del usuario para elegir el tipo de registro (puedes hacer clic en botones, enlaces, etc.)
        # Por ejemplo:
        register_particular_button = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.ID, 'register_company_button'))
        )
        register_particular_button.click()

        # Verifica que se haya redirigido correctamente a la vista de registro de empleado
        self.assertIn('/register_company', self.selenium.current_url)

        # Completa el formulario de usuario
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('testuser')

        first_name_input = self.selenium.find_element_by_name('first_name')
        first_name_input.send_keys('John')

        last_name_input = self.selenium.find_element_by_name('last_name')
        last_name_input.send_keys('Doe')

        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('test@example.com')

        password1_input = self.selenium.find_element_by_name('password1')
        password1_input.send_keys('parkour%123')

        password2_input = self.selenium.find_element_by_name('password2')
        password2_input.send_keys('parkour%123')

        # Completa el formulario de compañía
        name_input = self.selenium.find_element_by_name('name')
        name_input.send_keys('Test Catering Company')

        address_input = self.selenium.find_element_by_name('address')
        address_input.send_keys('123 Test St.')

        phone_number_input = self.selenium.find_element_by_name('phone_number')
        phone_number_input.send_keys('+12125552368')

        cif_input = self.selenium.find_element_by_name('cif')
        cif_input.send_keys('A1234567J')

        verification_document_input = self.selenium.find_element_by_name('verification_document')
        verification_document_input.send_keys(ruta_archivo)

        # Completa la casilla de Política de Privacidad
        privacy_policy_checkbox = self.selenium.find_element_by_id('privacyPolicy')
        privacy_policy_checkbox.click()

        # Envía el formulario
        submit_button = self.selenium.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # Verifica que se haya redirigido a la página de inicio después del registro exitoso
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/')  # URL de la página de inicio


class VisualAddMenuTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH)
        self.driver.implicitly_wait(10)

        # Crear usuario y empresa de catering
        self.user = CustomUser.objects.create_user(username='testuser', password='password',email='testuser@gmail.com')
        self.catering_company = CateringCompany.objects.create(user=self.user, name='Test Catering Company')

    def tearDown(self):
        self.driver.quit()

    def test_add_menu_authenticated_user(self):
        # Iniciar sesión con Selenium
        self.driver.get(self.live_server_url + '/login')
        self.driver.find_element_by_name('username').send_keys('testuser@gmail.com')
        self.driver.find_element_by_name('password').send_keys('password')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()

        # Navegar a la página para agregar un plato
        self.driver.get(self.live_server_url + '/add_menu/')
        # Rellenar el formulario

        name_input = self.driver.find_element_by_name('name')
        name_input.send_keys('Test Menu')
        description_input = self.driver.find_element_by_name('description')
        description_input.send_keys('This is a test menu')
        diet_restrictions_input = self.driver.find_element_by_name('diet_restrictions')
        diet_restrictions_input.send_keys('No restrictions')

        # Enviar el formulario
        self.driver.find_element_by_css_selector('button[type="submit"]').click()

        # Verificar si el plato se creó correctamente
        self.assertEqual(self.driver.current_url, self.live_server_url + '/list_menus/')
        success_message = self.driver.find_element_by_css_selector('.alert-success').text
        self.assertIn('Menu created successfully', success_message)


class VisualEditMenuTest(StaticLiveServerTestCase):
    def setUp(self):
        self.username = 'testuser@gmail.com'
        self.password = 'password'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)
        self.catering_company = CateringCompany.objects.create(user=self.user, name='Test Catering Company')
        self.menu = Menu.objects.create(cateringcompany=self.catering_company, name='Test Menu', description='Test Description', diet_restrictions='No restrictions')
        self.url = self.live_server_url + reverse('edit_menu', kwargs={'menu_id': self.menu.id})
        self.delete_url = self.live_server_url + reverse('delete_menu', kwargs={'menu_id': self.menu.id})

        self.driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_edit_menu_authenticated_user(self):
        # Iniciar sesión
        self.driver.get(self.live_server_url + '/login')
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_css_selector('button[type="submit"]').click()

        # Acceder a la página de edición del menú
        self.driver.get(self.url)

        # Simular la edición del menú
        name_input = self.driver.find_element_by_css_selector('input[name="name"]')
        name_input.clear()  # Limpiar el campo de nombre
        name_input.send_keys('Updated Menu')  # Introducir un nombre actualizado
        description_input = self.driver.find_element_by_css_selector('textarea[name="description"]')
        description_input.clear()
        description_input.send_keys('Updated Description')
        diet_restrictions_input = self.driver.find_element_by_css_selector('input[name="diet_restrictions"]')
        diet_restrictions_input.clear()
        diet_restrictions_input.send_keys('Updated Restrictions')

        # Enviar el formulario (método PUT simulado)
        self.driver.find_element_by_css_selector('button[type="submit"]').click()

        # Verificar si el menú se actualizó correctamente
        updated_menu = Menu.objects.get(id=self.menu.id)
        self.assertEqual(updated_menu.name, 'Updated Menu')
        self.assertEqual(updated_menu.description, 'Updated Description')
        self.assertEqual(updated_menu.diet_restrictions, 'Updated Restrictions')
    
    def test_delete_menu(self):
        # Ir a la página de lista de menús
        self.driver.get(self.live_server_url + '/login')
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_css_selector('button[type="submit"]').click()

        self.driver.get(f'{self.live_server_url}/list_menus/')
        
        # Encontrar el botón de eliminar y hacer clic en él
        delete_button = self.driver.find_element_by_name('delete_menu_button')
        if delete_button.is_displayed():
            delete_button.click()

        # Verificar si el menú fue eliminado correctamente
        self.assertNotIn(self.menu.name, self.driver.page_source)



class CateringCalendarViewTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(executable_path=settings.DRIVER_PATH)
        cls.email = 'testuser@gmail.com'
        cls.password = 'password'
        cls.user = CustomUser.objects.create_user(username=cls.email, password=cls.password)
        cls.catering_company = CateringCompany.objects.create(user=cls.user, name='Test Catering Company',price_plan="PREMIUM_PRO")

        cls.catering_service = CateringService.objects.create(
            cateringcompany=cls.catering_company,
            name="Mi servicio de catering",
            description="Descripción de mi servicio de catering",
            location="Ubicación de mi servicio de catering",
            capacity=100,
            price=500.00,
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

    def test_catering_calendar_view(self):
        # Iniciar sesión
        self.selenium.get(self.live_server_url + reverse('login'))
        self.selenium.find_element_by_name('username').send_keys(self.email)
        self.selenium.find_element_by_name('password').send_keys(self.password)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        # Abre la página del calendario de catering
        catering_calendar_url = reverse('catering_calendar', kwargs={'catering_service_id': self.catering_service.id, 'year': 2024, 'month': 4})
        self.selenium.get(self.live_server_url + catering_calendar_url)

        # Verifica que se muestre el nombre del catering y el año/mes actual
        h1_element = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        # Verifica si el texto esperado está presente en el elemento h1
        self.assertIn('Events on', h1_element.text)

        # Verificar la presencia del enlace "Previous Month"
        prev_month_link = self.selenium.find_element_by_link_text('Previous Month')
        self.assertIsNotNone(prev_month_link)

        # Verificar la presencia del enlace "Next Month"
        next_month_link = self.selenium.find_element_by_link_text('Next Month')
        self.assertIsNotNone(next_month_link)

        # Verifica que se muestre la tabla del calendario
        calendar_table = self.selenium.find_element_by_class_name("calendar-table")
        self.assertIsNotNone(calendar_table)

        # Verifica que se muestren los días del mes actual
        days_in_month = calendar_table.find_elements_by_xpath("//td")
        self.assertTrue(len(days_in_month) > 0)

        # Verifica que se muestre la información adicional
        info_section = self.selenium.find_element_by_class_name("info")
        next_event_info = info_section.find_element_by_xpath("//p[contains(text(), 'Next Event:')]")
        num_events_info = info_section.find_element_by_xpath("//p[contains(text(), 'Number of events this month:')]")

        self.assertIsNotNone(next_event_info)
        self.assertIsNotNone(num_events_info)

    def test_next_month_view(self):
        # Iniciar sesión
        self.selenium.get(self.live_server_url + reverse('login'))
        self.selenium.find_element_by_name('username').send_keys(self.email)
        self.selenium.find_element_by_name('password').send_keys(self.password)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        # Obtener la fecha actual
        current_date = datetime.now()

        # Calcular el mes siguiente
        next_date = current_date + timedelta(days=30)



        # Abre la página del calendario de catering
        next_month_url = reverse('next_month', kwargs={'catering_service_id': self.catering_service.id, 'year': next_date.year, 'month': next_date.month})
        self.selenium.get(self.live_server_url + next_month_url)

        # Verificar si la redirección a la página del próximo mes es exitosa
        self.assertIn('catering-calendar', self.selenium.current_url)

        # Obtener los parámetros de la URL
        url_params = next_month_url.split('/')
        year_param = int(url_params[-4])
        month_param = int(url_params[-3])

        # Verificar si la fecha en la URL corresponde al mes siguiente
        self.assertEqual(year_param, next_date.year)
        self.assertEqual(month_param, next_date.month)

    def test_prev_month_view(self):
        # Iniciar sesión
        self.selenium.get(self.live_server_url + reverse('login'))
        self.selenium.find_element_by_name('username').send_keys(self.email)
        self.selenium.find_element_by_name('password').send_keys(self.password)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        # Obtener la fecha actual
        current_date = datetime.now()

        # Calcular el mes anterior
        prev_date = current_date - timedelta(days=30)

        # Abre la página del calendario de catering
        prev_month_url = reverse('prev_month', kwargs={'catering_service_id': self.catering_service.id, 'year': prev_date.year, 'month': prev_date.month})
        self.selenium.get(self.live_server_url + prev_month_url)

        # Verificar si la redirección a la página del mes anterior es exitosa
        self.assertIn('catering-calendar', self.selenium.current_url)

        # Obtener los parámetros de la URL
        url_params = prev_month_url.split('/')
        year_param = int(url_params[-4])
        month_param = int(url_params[-3])

        # Verificar si la fecha en la URL corresponde al mes anterior
        self.assertEqual(year_param, prev_date.year)
        self.assertEqual(month_param, prev_date.month)  


    


