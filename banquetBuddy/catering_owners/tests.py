from django.test import TestCase
from core.models import Employee, Offer, JobApplication, CustomUser, CateringService, CateringCompany
from .views import employee_applications
from decimal import Decimal
from django.urls import reverse
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib.auth import authenticate
from .forms import EmployeeFilterForm


# Create your tests here.

class ViewTests(TestCase):
    
    def setUp(self) -> None:
        
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='testuser@gmail.com')
        self.catering_company = CateringCompany.objects.create(user=self.user, name='Prueba', phone_number=PhoneNumber.from_string("+15551234567"), service_description='Prueba', price_plan='PREMIUM_PRO')
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
