from asyncio import Task
import os
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse

from .models import Employee
from catering_particular.models import Particular
from core.models import CustomUser
from catering_owners.models import *
from .views import *
from django.urls import reverse
from datetime import datetime, timedelta, date
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class EmployeeTestCases(TestCase):

    def create_event(self):

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
            cateringcompany=self.catering_company,
            particular=self.particular1,
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
            cateringcompany=self.catering_company,
            description="Test Task Description",
            assignment_date=datetime.now().date(),
            assignment_state="COMPLETED",
            expiration_date=expiration_date,
            priority="HIGH",
        )
        self.task.employees.add(self.employee)

    def setUp(self):
        self.factory = RequestFactory()
        self.user_employee1 = CustomUser.objects.create_user(
            username="testuser_employee1", password="12345", email="employee@gmail.com"
        )

        self.user_employee2 = CustomUser.objects.create_user(
            username="testuser_employee2",
            email="employee2@example.com",
            password="testpassword4",
        )

        self.user_catering_company = CustomUser.objects.create_user(
            username="testuser_catering_company",
            password="12345",
            email="cateringCompany@gmail.com",
        )

        self.employee = Employee.objects.create(
            user=self.user_employee1,
            phone_number="123456789",
            profession="Tester",
            experience="5 years",
            skills="Testing skills",
            english_level="ALTO",
            location="Test Location",
        )

        self.employee2 = Employee.objects.create(
            user=self.user_employee2,
            phone_number="123456789",
            profession="Tester",
            experience="5 years",
            skills="Testing skills",
            english_level="ALTO",
            location="Test Location",
        )

        self.catering_company = CateringCompany.objects.create(
            user=self.user_catering_company,
            name="Test Catering Company",
            address="Test Address",
            phone_number="987654321",
            cif="123456789A",
            is_verified=True,
            price_plan="Basic",
        )

        self.catering_service = CateringService.objects.create(
            cateringcompany=self.catering_company,
            name="Test Catering Service",
            description="Test Description",
            location="Test Location",
            capacity=100,
            price=100.00,
        )

        self.create_particular()
        self.create_event()

        self.offer = Offer.objects.create(
            cateringservice=self.catering_service,
            event=self.event,
            title="Test Offer",
            description="Test Description",
            requirements="Test Requirements",
            location="Test Location",
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=1),
        )

        curriculum_path = os.path.join(
            settings.MEDIA_ROOT, "curriculums", "curriculum.pdf"
        )

        if os.path.exists(curriculum_path):
            with open(curriculum_path, "rb") as f:
                self.employee.curriculum.save("curriculum.pdf", File(f))

    def create_particular(self):

        self.user_particular1 = CustomUser.objects.create_user(
            username="testuser_particular1",
            email="particular1@example.com",
            password="testpassword2",
        )

        self.particular1 = Particular.objects.create(
            user=self.user_particular1,
            phone_number="123456789",
            preferences="Test preferences",
            address="Test address",
            is_subscribed=False,
        )

    def create_specific_job_application(self):

        self.job_application = JobApplication.objects.create(
            employee=self.employee, offer=self.offer, state="PENDING"
        )

    def create_recommendation_letter(self):
        self.recommendation = RecommendationLetter.objects.create(
            employee=self.employee,
            catering=self.catering_company,
            description="Test Recommendation Letter Description",
            date=datetime.now().date(),
        )

    # Test para la vista de lista de ofertas de empleo
    def test_employee_offer_list_view(self):
        request = self.factory.get(reverse("employeeOfferList"))
        request.user = self.user_employee1
        response = employee_offer_list(request)

        self.assertEqual(response.status_code, 200)

    def test_employee_offer_list_view_with_anonymous_user(self):
        request = self.factory.get(reverse("employeeOfferList"))
        request.user = AnonymousUser()
        response = employee_offer_list(request)

        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_employee_offer_list_view(self):
        request = self.factory.get(reverse("employeeOfferList"))
        request.user = self.user_employee1
        response = employee_offer_list(request)  # Cambio aquí

        self.assertEqual(response.status_code, 200)

    def test_employee_offer_list_view_with_anonymous_user(self):
        request = self.factory.get(reverse("employeeOfferList"))
        request.user = AnonymousUser()
        response = employee_offer_list(request)  # Cambio aquí

        self.assertEqual(response.status_code, 302)

    # Test para la vista de solicitud de empleo
    def test_application_to_offer_view_successful_application(self):
        request = self.factory.get(
            reverse("application_to_offer", args=[self.offer.id])
        )
        request.user = self.user_employee1
        response = application_to_offer(request, self.offer.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            JobApplication.objects.filter(
                employee=self.employee, offer=self.offer
            ).exists()
        )

    def test_application_to_offer_view_invalid_employee(self):
        invalid_user = CustomUser.objects.create_user(
            username="invaliduser", password="12345", email="prueba@gmail.com"
        )

        request = self.factory.get(
            reverse("application_to_offer", args=[self.offer.id])
        )
        request.user = invalid_user
        response = application_to_offer(request, self.offer.id)

        self.assertEqual(
            response.status_code, 200
        )  # Renders error template for invalid employee

    def test_application_to_offer_view_already_applied(self):
        JobApplication.objects.create(
            employee=self.employee, offer=self.offer, state="PENDING"
        )
        request = self.factory.get(
            reverse("application_to_offer", args=[self.offer.id])
        )
        request.user = self.user_employee1
        response = application_to_offer(request, self.offer.id)

        self.assertEqual(
            response.status_code, 200
        )  # Renders error template for already applied

    def test_application_to_offer_view_no_curriculum(self):
        self.employee.curriculum.delete()
        request = self.factory.get(
            reverse("application_to_offer", args=[self.offer.id])
        )
        request.user = self.user_employee1
        response = application_to_offer(request, self.offer.id)

        self.assertEqual(response.status_code, 200)

    # Test para la vista de lista de aplicaciones de empleo
    def test_employee_applications_list_authenticated_employee(self):
        self.client.force_login(self.user_employee1)
        job_application = JobApplication.objects.create(
            employee=self.employee, offer=self.offer, date_application=date.today()
        )
        response = self.client.get(reverse("JobApplicationList"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(job_application, response.context["applications"])

    def test_employee_applications_list_authenticated_non_employee(self):
        non_employee_user = CustomUser.objects.create_user(
            username="nonemployee", email="nonemployee@example.com", password="password"
        )
        self.client.force_login(non_employee_user)
        response = self.client.get(reverse("JobApplicationList"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "error_employee.html")

    def test_employee_applications_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("JobApplicationList"))

        self.assertEqual(response.status_code, 302)

    # Test para la vista de notificación de aplicación de empleo
    def test_notify_employee_state(self):
        self.create_specific_job_application()
        self.job_application.state = "PENDING"
        self.job_application.save()
        notification = NotificationJobApplication.objects.filter(
            user=self.user_employee1, job_application=self.job_application
        ).count()

        assert notification != 0

    # Test para la vista de recommendation letters
    def test_my_recommendation_letters_view_authenticated(self):
        self.create_recommendation_letter()
        self.client.force_login(self.user_employee1)
        response = self.client.get(
            reverse("my_recommendation_letters", args=[self.employee.user.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_other_recommendation_letters_view(self):
        self.create_recommendation_letter()
        self.client.force_login(self.user_employee2)
        response = self.client.get(
            reverse("my_recommendation_letters", args=[self.employee.user.id])
        )

        self.assertEqual(response.status_code, 403)

    def test_no_employee_recommendation_letters_view(self):
        self.create_recommendation_letter()
        self.client.force_login(self.user_catering_company)
        response = self.client.get(
            reverse("my_recommendation_letters", args=[self.employee.user.id])
        )

        self.assertEqual(response.status_code, 403)

    def test_my_recommendation_letters_view_unauthenticated(self):
        self.create_recommendation_letter()
        response = self.client.get(
            reverse("my_recommendation_letters", args=[self.employee.user.id])
        )

        self.assertEqual(response.status_code, 302)


class ListarCateringsCompaniesTestCase(TestCase):
    def setUp(self):
        # Configuración inicial para crear un usuario de prueba
        self.factory = RequestFactory()

        # Creamos un usuario de prueba
        self.employee_user = CustomUser.objects.create_user(
            username="employee_user", email="employee@example.com", password="password"
        )

        # Creamos un empleado asociado con el usuario
        self.employee = Employee.objects.create(user=self.employee_user)

    def test_listar_caterings_companies_employee_authenticated(self):
        # Autenticamos al usuario como empleado
        self.client.force_login(self.employee_user)

        # Realizamos una solicitud GET a la vista
        response = self.client.get(reverse("listar_caterings_companies_employee"))

        # Verificamos que la vista responda correctamente
        self.assertEqual(response.status_code, 200)

        # Verificamos que la lista de empresas de catering esté presente en el contexto
        self.assertIn("caterings", response.context)

    def test_listar_caterings_companies_employee_unauthenticated(self):
        # Realizamos una solicitud GET a la vista sin autenticar al usuario
        response = self.client.get(reverse("listar_caterings_companies_employee"))

        # Verificamos que el usuario no autenticado reciba un código de estado 403
        self.assertEqual(response.status_code, 403)


class RegisterEmployeeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse(
            "register_employee"
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
                "phone_number": "+34666666666",
                "profession": "Tester",
                "experience": "5 years",
                "skills": "Testing skills",
                "curriculum": pdf_file,
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
