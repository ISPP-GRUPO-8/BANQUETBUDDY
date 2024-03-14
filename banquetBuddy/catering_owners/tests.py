from decimal import Decimal

import os
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from catering_employees.forms import EmployeeFilterForm
from catering_employees.models import Employee
from catering_owners.models import CateringCompany, CateringService, JobApplication, Offer

from core.forms import CustomUserCreationForm
from .forms import CateringCompanyForm
from core.models import CustomUser
from phonenumbers import PhoneNumber, parse, is_valid_number

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
        phone_number = parse("+15551234567", "US")
        self.catering_company = CateringCompany.objects.create(user=self.user, name='Prueba', phone_number=str(phone_number), service_description='Prueba', price_plan='PREMIUM_PRO')
        self.catering_service = CateringService.objects.create(
            cateringcompany=self.catering_company,
            name="Brunch para la oficina",
            description="Delicioso brunch con variedad de opciones dulces y saladas perfecto para reuniones de trabajo.",
            location="Calle Mayor, 123",
            capacity=50,
            price=Decimal("129.99"),
        )
        self.offer = Offer.objects.create(title="Oferta de prueba", description="Descripción de prueba", requirements="Requisitos de prueba", location="Ubicación de prueba",cateringservice= self.catering_service)
        self.employee = Employee.objects.create(user=CustomUser.objects.create(username="usuario_prueba", email= 'estoesunaprueba@gmail.com'), phone_number="1234567890", profession="Chef", experience="5 years", skills="Culinary skills", english_level="C2", location="Ubicación de prueba")
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
        
    def tearDown(self) -> None:
        self.user.delete()
        self.catering_company.delete()
        self.catering_service.delete()
        self.offer.delete()
        self.employee.delete()
        self.job_application.delete()
