from django.test import TestCase
from core.models import Employee, Offer, JobApplication, CustomUser, CateringService, CateringCompany
from .views import employee_applications
from decimal import Decimal
from phonenumber_field.phonenumber import PhoneNumber

# Create your tests here.

class ViewTests(TestCase):

    def test_get_applicants(self):
        
        user_catering=CustomUser.objects.create(username="usuario_prueba_catering", email= 'estoesunaprueba1@gmail.com')
        
        catering_company = CateringCompany.objects.create(user=user_catering, name='Prueba', phone_number=PhoneNumber.from_string("+15551234567"), service_description='Prueba', price_plan='PREMIUM_PRO')
        
        catering_service = CateringService.objects.create(
            cateringcompany=catering_company,
            name="Brunch para la oficina",
            description="Delicioso brunch con variedad de opciones dulces y saladas perfecto para reuniones de trabajo.",
            location="Calle Mayor, 123",
            capacity=50,
            price=Decimal("129.99"),
        )
        # Crea una oferta de prueba
        offer = Offer.objects.create(title="Oferta de prueba", description="Descripción de prueba", requirements="Requisitos de prueba", location="Ubicación de prueba",cateringservice= catering_service)

        # Crea un empleado de prueba
        employee = Employee.objects.create(user=CustomUser.objects.create(username="usuario_prueba", email= 'estoesunaprueba@gmail.com'), phone_number="1234567890", profession="Profesión de prueba", experience="Experiencia de prueba", skills="Habilidades de prueba", english_level="B2", location="Ubicación de prueba")

        # Crea una solicitud de trabajo de prueba
        JobApplication.objects.create(employee=employee, offer=offer, date_application="2023-11-14", state="APLICADO")

        # Simula una solicitud HTTP a la vista
        response = self.client.get(f"/applicants/{offer.id}/")

        # Comprueba el código de respuesta HTTP
        self.assertEqual(response.status_code, 200)

        # Comprueba que la plantilla correcta se ha renderizado
        self.assertTemplateUsed(response, "applicants_list.html")

        # Comprueba que la lista de solicitantes contiene el empleado de prueba
        applicants = response.context['applicants']
        self.assertEqual(len(applicants), 1)
        self.assertEqual(applicants[0].employee.user.username, "usuario_prueba")