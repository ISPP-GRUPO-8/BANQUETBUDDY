from decimal import Decimal
import os
from django.test import Client, TestCase
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


class CateringBookTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.user1 = CustomUser.objects.create_user(
            username="testuser2", email="test2@example.com", password="testpassword2"
        )

        self.company = CateringCompany.objects.create(
            user=self.user,
            name="Test Catering Company",
            phone_number="123456789",
            service_description="Test service description",
            price_plan="BASE",
        )

        self.particular = Particular.objects.create(
            user=self.user1,
            phone_number="123456789",
            preferences="Test preferences",
            address="Test address",
            is_subscribed=False,
        )

        self.catering_service = CateringService.objects.create(
            cateringcompany=self.company,
            name="Test Catering Service",
            description="Test service description",
            location="Test location",
            capacity=100,
            price=100.00,
        )

        self.menu = Menu.objects.create(
            id=1,
            cateringservice=self.catering_service,
            name="Test Menu",
            description="Test menu description",
            diet_restrictions="Test diet restrictions",
        )
        self.catering_service.menus.add(self.menu)

        self.menu2 = Menu.objects.create(
            id=2,
            cateringservice=self.catering_service,
            name="Test Menu 2",
            description="Test menu description 2",
            diet_restrictions="Test diet restrictions 2",
        )
        self.catering_service.menus.add(self.menu2)

        self.event = Event.objects.create(
            cateringservice=self.catering_service,
            particular=self.particular,
            cateringcompany=self.company,
            menu=self.menu,
            name="Test Event",
            date=datetime.now().date(),
            details="Test details",
            booking_state=BookingState.CONTRACT_PENDING,
            number_guests=23,
        )

        self.client = Client()

    def test_my_books_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("catering_books"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "particular_books.html")

    def test_my_books_view_not_authorized(self):
        response = self.client.get(reverse("catering_books"))
        self.assertEqual(response.status_code, 302)

    # def test_book_edit_view(self):
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse('catering_books_edit', args=[self.event.id]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'catering_book_edit.html')

    #     response = self.client.post(reverse('catering_books_edit', args=[self.event.id]), {
    #         'date': '2024-04-15',
    #         'number_guests': '10',
    #         'selected_menu': self.menu2.id, 
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     edited_event = Event.objects.get(id=self.event.id)
    #     self.assertEqual(edited_event.date.strftime('%Y-%m-%d'), '2024-04-15')
    #     self.assertEqual(edited_event.number_guests, 10)
    #     self.assertEqual(edited_event.menu, self.menu2)
    #     self.assertEqual(edited_event.booking_state, BookingState.CONTRACT_PENDING)
    
    def test_book_edit_view_incomplete_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("catering_books_edit", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catering_book_edit.html")

        response = self.client.post(
            reverse("catering_books_edit", args=[self.event.id]),
            {
                "date": "2024-03-15",
                "number_guests": "0",
                "selected_menu": self.menu2.id,
            },
        )
        self.assertEqual(response.status_code, 200)

        edited_event = Event.objects.get(id=self.event.id)
        self.assertEqual(edited_event.date, self.event.date)
        self.assertEqual(edited_event.number_guests, self.event.number_guests)
        self.assertEqual(edited_event.menu, self.event.menu)
        self.assertEqual(edited_event.booking_state, self.event.booking_state)

    def test_book_edit_view_past_date(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("catering_books_edit", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catering_book_edit.html")

        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.post(
            reverse("catering_books_edit", args=[self.event.id]),
            {
                "date": past_date,
                "number_guests": "10",
                "selected_menu": self.menu2.id,
            },
        )

        self.assertEqual(response.status_code, 200)

        edited_event = Event.objects.get(id=self.event.id)
        self.assertEqual(edited_event.date, self.event.date)
        self.assertEqual(edited_event.number_guests, self.event.number_guests)
        self.assertEqual(edited_event.menu, self.event.menu)
        self.assertEqual(edited_event.booking_state, self.event.booking_state)

    def test_book_cancel_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("catering_books_cancel", args=[self.event.id])
        )
        self.assertEqual(response.status_code, 302)
        canceled_event = Event.objects.get(id=self.event.id)
        self.assertEqual(canceled_event.booking_state, BookingState.CANCELLED)


class RegisterCompanyTestCase(TestCase):
    def test_register_company_view(self):
        response = self.client.get(reverse("register_company"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registro_company.html")

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
        file_path = os.path.join(os.path.dirname(__file__), "test_files", file_name)

        # Lee el contenido del archivo PDF
        with open(file_path, "rb") as file:
            file_content = file.read()

        # Crea el objeto SimpleUploadedFile con el contenido del archivo PDF
        file_mock = SimpleUploadedFile(
            file_name, file_content, content_type="application/pdf"
        )

        user_data = {
            "username": "user_cool",
            "first_name": "Test",
            "last_name": "User",
            "email": "emailtest@gmail.com",
            "password1": "easy_password",
            "password2": "easy_password",
        }

        user_form = CustomUserCreationForm(data=user_data)
        print(user_form.errors)
        self.assertTrue(user_form.is_valid())
        user = user_form.save()

        form_data = {
            "username": "user_cool",
            "first_name": "Test",
            "last_name": "User",
            "email": "emailtest@gmail.com",
            "password1": "easy_password",
            "password2": "easy_password",
            "name": "Test Company",
            "address": "Test Address",
            "phone_number": "+34666555444",
            "cif": "A1234567J",
            "price_plan": "BASE",
        }
        files = {"verification_document": file_mock}

        form = CateringCompanyForm(data=form_data, files=files)

        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):

    def setUp(self) -> None:

        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@gmail.com"
        )
        self.user_particular = CustomUser.objects.create_user(
            username="testuser2", password="testpassword", email="testuser2@gmail.com"
        )
        phone_number = parse("+15551234567", "US")
        self.catering_company = CateringCompany.objects.create(
            user=self.user,
            name="Prueba",
            phone_number=str(phone_number),
            service_description="Prueba",
            price_plan="PREMIUM_PRO",
        )
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
            id=1,
            cateringservice=self.catering_service,
            name="Test Menu",
            description="Test menu description",
            diet_restrictions="Test diet restrictions",
        )
        self.event = Event.objects.create(
            cateringservice=self.catering_service,
            particular=self.particular,
            cateringcompany=self.catering_company,
            menu=self.menu,
            name="Test Event",
            date=datetime.now().date(),
            details="Test details",
            booking_state=BookingState.CONTRACT_PENDING,
            number_guests=23,
        )
        self.offer = Offer.objects.create(
            title="Oferta de prueba",
            event=self.event,
            description="Descripción de prueba",
            requirements="Requisitos de prueba",
            location="Ubicación de prueba",
            cateringservice=self.catering_service,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=1),
        )
        self.employee = Employee.objects.create(
            user=CustomUser.objects.create(
                username="usuario_prueba", email="estoesunaprueba@gmail.com"
            ),
            phone_number="1234567890",
            profession="Chef",
            experience="5 years",
            skills="Culinary skills",
            english_level="C2",
            location="Ubicación de prueba",
        )

        curriculum_path = os.path.join(
            settings.MEDIA_ROOT, "curriculums", "curriculum.pdf"
        )

        if os.path.exists(curriculum_path):
            with open(curriculum_path, "rb") as f:
                self.employee.curriculum.save("curriculum.pdf", File(f))

        self.job_application = JobApplication.objects.create(
            employee=self.employee,
            offer=self.offer,
            date_application="2023-11-14",
            state="APLICADO",
        )

    def test_get_applicants(self):

        self.client.force_login(self.user)

        # Simula una solicitud HTTP a la vista
        response = self.client.get(f"/applicants/{self.offer.id}/")

        # Comprueba el código de respuesta HTTP
        self.assertEqual(response.status_code, 200)

        # Comprueba que la plantilla correcta se ha renderizado
        self.assertTemplateUsed(response, "applicants_list.html")

        # Comprueba que la lista de solicitantes contiene el empleado de prueba
        applicants = response.context["applicants"]
        self.assertEqual(len(applicants), 1)
        self.assertEqual(applicants[0].employee.user.username, "usuario_prueba")

    def test_employee_filter_form(self):
        # Crea datos para el formulario de filtro
        data = {
            "english_level": "C2",
            "profession": "Chef",
            "experience": "5 years",
            "skills": "Culinary skills",
        }

        # Crea una instancia del formulario de filtro con los datos
        form = EmployeeFilterForm(data)

        # Verifica que el formulario sea válido
        self.assertTrue(form.is_valid())

        # Obtén el queryset original de la vista
        original_queryset = self.offer.job_applications.select_related("employee").all()

        # Filtra el queryset con el formulario
        filtered_queryset = form.filter_queryset(original_queryset)

        # Verifica que el queryset filtrado tenga el tamaño esperado (1 en este caso)
        self.assertEqual(filtered_queryset.count(), 1)

    def test_profile_edit_view_get(self):
        # Prueba GET request a la vista
        self.client.force_login(self.user)
        response = self.client.get(reverse("catering_profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_company_edit.html")

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

        self.user = CustomUser.objects.create_user(
            username="test_user", password="test_password", email="testuser@gmail.com"
        )
        self.user2 = CustomUser.objects.create_user(
            username="test_user2", password="test_password2"
        )

        self.catering_company = CateringCompany.objects.create(
            user=self.user, name="Test Catering Company", price_plan="PREMIUM_PRO"
        )
        self.catering_company2 = CateringCompany.objects.create(
            user=self.user2, name="Catering Company 2", price_plan="PREMIUM"
        )
        self.catering_service = CateringService.objects.create(
            name="Test Catering",
            cateringcompany=self.catering_company,
            description="Test description",
            location="Test location",
            capacity=100,
            price=500.00,
        )
        self.particular = Particular.objects.create(user=self.user)
        self.menu = Menu.objects.create(name="Test Menu")
        self.event_date = datetime.now().date()
        self.event = Event.objects.create(
            cateringservice=self.catering_service,
            particular=self.particular,
            cateringcompany=self.catering_company,
            menu=self.menu,
            name="Test Event",
            date=self.event_date,
            details="Test details",
            booking_state=BookingState.choices[0][0],
            number_guests=10,
        )

    def test_view_reservations_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "view_reservations",
                kwargs={"catering_service_id": self.catering_service.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations.html")

    def test_view_reservation_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "view_reservation",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "event_id": self.event.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_reservation.html")

    def test_catering_calendar_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "catering_calendar",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": self.event_date.year,
                    "month": self.event_date.month,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calendar.html")

    def test_reservations_for_day_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "reservations_for_day",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": self.event_date.year,
                    "month": self.event_date.month,
                    "day": self.event_date.day,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations_for_day.html")

    def test_next_month_view_authenticated(self):
        # Prueba para avanzar al mes siguiente en el calendario cuando el usuario está autenticado
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "next_month",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": self.event_date.year,
                    "month": self.event_date.month,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        next_month_date = self.event_date.replace(day=1) + timedelta(
            days=32
        )  # Obtener la fecha del mes siguiente
        self.assertRedirects(
            response,
            reverse(
                "catering_calendar",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": next_month_date.year,
                    "month": next_month_date.month,
                },
            ),
        )

    def test_prev_month_view_authenticated(self):
        # Prueba para retroceder al mes anterior en el calendario cuando el usuario está autenticado
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "prev_month",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": self.event_date.year,
                    "month": self.event_date.month,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        prev_month_date = self.event_date.replace(day=1) - timedelta(
            days=1
        )  # Obtener la fecha del mes anterior
        self.assertRedirects(
            response,
            reverse(
                "catering_calendar",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": prev_month_date.year,
                    "month": prev_month_date.month,
                },
            ),
        )

    def test_permission_denied(self):
        # Intentar acceder a las vistas protegidas sin iniciar sesión
        self.client.force_login(self.user2)
        response_view_reservations = self.client.get(
            reverse(
                "view_reservations",
                kwargs={"catering_service_id": self.catering_service.pk},
            )
        )
        response_view_reservation = self.client.get(
            reverse(
                "view_reservation",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "event_id": self.event.pk,
                },
            )
        )
        response_catering_calendar = self.client.get(
            reverse(
                "catering_calendar",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": self.event_date.year,
                    "month": self.event_date.month,
                },
            )
        )
        response_reservations_for_day = self.client.get(
            reverse(
                "reservations_for_day",
                kwargs={
                    "catering_service_id": self.catering_service.pk,
                    "year": self.event_date.year,
                    "month": self.event_date.month,
                    "day": self.event_date.day,
                },
            )
        )

        # Verificar si se devuelve un error de permiso
        self.assertEqual(response_view_reservations.status_code, 403)
        self.assertEqual(response_view_reservation.status_code, 403)
        self.assertEqual(response_catering_calendar.status_code, 403)
        self.assertEqual(response_reservations_for_day.status_code, 403)


class RecommendationLetterTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.user1 = CustomUser.objects.create_user(
            username="testuser2", email="test2@example.com", password="testpassword2"
        )
        self.user2 = CustomUser.objects.create_user(
            username="testuser3", email="test3@example.com", password="testpassword3"
        )

        self.company = CateringCompany.objects.create(
            user=self.user,
            name="Test Catering Company",
            phone_number="123456789",
            service_description="Test service description",
            price_plan="BASE",
        )

        self.particular = Particular.objects.create(
            user=self.user1,
            phone_number="123456789",
            preferences="Test preferences",
            address="Test address",
            is_subscribed=False,
        )

        self.employee = Employee.objects.create(
            user=self.user2,
            phone_number="123456789",
            profession="Tester",
            experience="5 years",
            skills="Testing skills",
            english_level="ALTO",
            location="Test Location",
        )

        curriculum_path = os.path.join(
            settings.MEDIA_ROOT, "curriculums", "curriculum.pdf"
        )

        if os.path.exists(curriculum_path):
            with open(curriculum_path, "rb") as f:
                self.employee.curriculum.save("curriculum.pdf", File(f))

        self.catering_service = CateringService.objects.create(
            cateringcompany=self.company,
            name="Test Catering Service",
            description="Test Description",
            location="Test Location",
            capacity=100,
            price=100.00,
        )

        self.menu = Menu.objects.create(
            id=1,
            cateringservice=self.catering_service,
            name="Test Menu",
            description="Test menu description",
            diet_restrictions="Test diet restrictions",
        )
        self.catering_service.menus.add(self.menu)

        self.event = Event.objects.create(
            cateringservice=self.catering_service,
            particular=self.particular,
            cateringcompany=self.company,
            menu=self.menu,
            name="Test Event",
            date=datetime.now().date(),
            details="Test details",
            booking_state=BookingState.CONTRACT_PENDING,
            number_guests=23,
        )
        expiration_date = datetime.now().date() + timedelta(days=1)
        self.task = Task.objects.create(
            event=self.event,
            cateringservice=self.catering_service,
            cateringcompany=self.company,
            description="Test Task Description",
            assignment_date=datetime.now().date(),
            assignment_state="COMPLETED",
            expiration_date=expiration_date,
            priority="HIGH",
        )
        self.task.employees.add(self.employee)

        self.recommendation = RecommendationLetter.objects.create(
            employee=self.employee,
            catering=self.company,
            description="Test Recommendation Letter Description",
            date=datetime.now().date(),
        )

    def test_list_employee_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("list_employee", args=[self.catering_service.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_employee.html")

    def test_recommendation_letter_creation_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "recommendation_letter",
                args=[self.catering_service.id, self.employee.user.id],
            ),
            {
                "description": "Description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            RecommendationLetter.objects.filter(employee=self.employee).exists()
        )

    def test_recommendation_letter_creation_unauthenticated(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse(
                "recommendation_letter",
                args=[self.catering_service.id, self.employee.user.id],
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_recommendation_letter_get_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "recommendation_letter",
                args=[self.catering_service.id, self.employee.user.id],
            )
        )
        self.assertEqual(response.status_code, 200)


class ChatViewTestCase(TestCase):
    def setUp(self):
        # Crear usuarios personalizados
        self.particular_user = CustomUser.objects.create_user(
            username="particular_user",
            email="particular@example.com",
            password="password",
        )
        self.employee_user = CustomUser.objects.create_user(
            username="employee_user", email="employee@example.com", password="password"
        )
        self.company_user = CustomUser.objects.create_user(
            username="company_user", email="company@example.com", password="password"
        )

        # Crear instancias de Particular, Employee y CateringCompany
        self.particular = Particular.objects.create(user=self.particular_user)
        self.employee = Employee.objects.create(user=self.employee_user)
        self.company = CateringCompany.objects.create(user=self.company_user)

        # Crear algunos mensajes
        Message.objects.create(
            sender=self.particular_user,
            receiver=self.company_user,
            date=timezone.now(),
            content="Hola desde el particular",
        )
        Message.objects.create(
            sender=self.company_user,
            receiver=self.particular_user,
            date=timezone.now(),
            content="Hola desde la empresa",
        )

    def test_chat_view_particular(self):
        # Prueba la vista de chat para un usuario particular
        self.client.force_login(self.particular_user)
        response = self.client.get("/chat/{}/".format(self.company.user.id))
        self.assertEqual(response.status_code, 200)

    def test_chat_view_employee(self):
        # Prueba la vista de chat para un empleado
        self.client.force_login(self.employee_user)
        response = self.client.get("/chat/{}/".format(self.company.user.id))
        self.assertEqual(response.status_code, 200)

    def test_chat_view_catering_company(self):
        # Prueba la vista de chat para una empresa de catering
        self.client.force_login(self.company_user)
        response = self.client.get("/chat/{}/".format(self.particular.user.id))
        self.assertEqual(response.status_code, 200)


class CateringViewTest(TestCase):
    def setUp(self):
        # Configurar el entorno de prueba con objetos necesarios
        self.client = Client()

        self.user = CustomUser.objects.create_user(
            username="test_user", password="test_password", email="testuser@gmail.com"
        )
        self.user1 = CustomUser.objects.create_user(
            username="test_user1",
            password="test_password1",
            email="testuser1@gmail.com",
        )

        self.catering_company = CateringCompany.objects.create(
            user=self.user, name="Test Catering Company", price_plan="PREMIUM_PRO"
        )

        self.message = Message.objects.create(
            sender=self.user,
            receiver=self.user1,
            date=datetime.now(),
            content="Este es un mensaje de ejemplo.",
        )

    def test_listar_caterings_particular(self):
        # Simular una solicitud HTTP al punto final
        self.client.force_login(self.user)

        # Realizar la solicitud HTTP
        response = self.client.get(reverse("listar_caterings_particular"))

        # Verificar si la respuesta es exitosa
        self.assertEqual(response.status_code, 200)

        # Verificar si el template utilizado es el esperado
        self.assertTemplateUsed(response, "contact_chat_owner.html")

        # Verificar si el contexto se pasa correctamente al template
        self.assertTrue(response.context["is_catering_company"])

        self.assertIn("messages", response.context)

    def test_listar_caterings_particular_unauthenticated(self):
        # Realizamos una solicitud GET a la vista sin autenticar al usuario
        response = self.client.get(reverse("listar_caterings_particular"))

        # Verificamos que el usuario no autenticado reciba un código de estado 302 para redirigirlo
        self.assertEqual(response.status_code, 302)


class RegisterCompanyTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse(
            "register_company"
        )  # Asegúrate de que 'register_particular' es el nombre correcto de la URL en tu archivo urls.py

    def test_register_particular_valid_data(self):
        User = get_user_model()
        user_count = User.objects.count()
        # Crea un archivo PDF de prueba
        pdf_content = (
            b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        )
        pdf_file = SimpleUploadedFile(
            "test.pdf", pdf_content, content_type="application/pdf"
        )

        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@test.com",
                "password1": "Hola12345",
                "password2": "Hola12345",
                "name": "Test Company",
                "address": "Test Address",
                "phone_number": "+34666666666",
                "cif": "A12345678",
                "verification_document": pdf_file,
                "privacyPolicy": True,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # 302 significa redirección, lo que indica que el registro fue exitoso
        self.assertEqual(
            User.objects.count(), user_count + 1
        )  # Comprueba que se creó un nuevo usuario
        user = User.objects.latest("id")
        self.assertEqual(
            user.is_active, False
        )  # Comprueba que la cuenta del usuario está desactivada

        # Ahora prueba la activación de la cuenta
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activate_url = reverse(
            "activate", kwargs={"uidb64": uid, "token": token}
        )  # Asegúrate de que este es el nombre correcto de la URL

        response = self.client.get(activate_url)
        self.assertEqual(
            response.status_code, 302
        )  # Debería haber una redirección después de la activación exitosa

        user.refresh_from_db()
        self.assertTrue(
            user.is_active
        )  # El usuario debería estar activo después de la activación


########################
###Tests de interfaz####
########################