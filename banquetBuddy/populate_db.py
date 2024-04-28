from datetime import timedelta
import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banquetBuddy.settings')
django.setup()
from django.core.files import File
from django.utils import timezone
from faker.providers import person, address
from django.conf import settings
from catering_employees.models import CustomUser, Employee, Message
from catering_owners.models import CateringCompany, CateringService, CuisineTypeModel, EmployeeWorkService, Event, JobApplication, Menu, Offer, Plate, Review, Task, RecommendationLetter
from catering_particular.models import Particular
from django.contrib.auth import get_user_model
import datetime
import decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


from faker import Faker
from core.models import *
from random import randint, choice
from django.utils.timezone import make_aware
from django.db import transaction
faker = Faker(['es_ES'])
faker.add_provider(person)
faker.add_provider(address)
CustomUser = get_user_model()



def truncate_all_tables():
    
    models_to_truncate = [
        Particular, CateringCompany, Employee, Message,
        CateringService, Event, Task, Menu, Review,
        EmployeeWorkService, Offer, JobApplication, CustomUser
    ]
    for model1 in models_to_truncate:
        model1.objects.all().delete()
    print("All data has been deleted from the database.")


def create_particulars():
    with open('populate/particulars.json', 'r', encoding='utf-8') as file:
        particulars = json.load(file)
        for p in particulars:
            user = CustomUser.objects.create_user(
                username=p['username'], 
                password=p['password'], 
                email=p['email']
            )
            Particular.objects.create(
                user=user,
                phone_number=p['phone_number'],
                preferences=", ".join(p['preferences']),
                address=p['address'],
                is_subscribed=p['is_subscribed']
            )




def create_catering_companies():
    with open('populate/catering_companies.json', 'r', encoding='utf-8') as file:
        companies = json.load(file)
        for company in companies:
            user = CustomUser.objects.create_user(
                username=company['username'], 
                password=company['password'], 
                email=company['email']
            )
            catering_company = CateringCompany.objects.create(
                user=user,
                name=company['name'],
                phone_number=company['phone_number'],
                service_description=company['service_description'],
                is_verified=company['is_verified'],
                price_plan=company['price_plan'],
                address=company['address']
            )
            for cuisine_type in company['cuisine_types']:
                cuisine, _ = CuisineTypeModel.objects.get_or_create(type=cuisine_type)
                catering_company.cuisine_types.add(cuisine)
            if company['logo']:
                logo_path = os.path.join(settings.MEDIA_ROOT, 'logos', company['logo'])
                if os.path.exists(logo_path):
                    with open(logo_path, 'rb') as f:
                        catering_company.logo.save(company['logo'], File(f), save=True)



def create_employees():
    with open('populate/employees.json', 'r', encoding='utf-8') as file:
        employees = json.load(file)
        for emp in employees:
            # Crear usuario asociado
            user = CustomUser.objects.create_user(
                username=emp['username'], 
                password=emp['password'], 
                email=emp['email']
            )
            # Crear instancia de empleado
            Employee.objects.create(
                user=user,
                profession=emp['profession'],
                experience=emp['experience'],
                skills=emp['skills'],
                english_level=emp['english_level'],
                location=emp['location'],
                curriculum=emp['curriculum']
            )


def create_messages():
    with open('populate/messages.json', 'r', encoding='utf-8') as file:
        messages_content = json.load(file)
        for message_data in messages_content:
            sender_username = message_data['sender']
            receiver_username = message_data['receiver']
            sender_particular = Particular.objects.get(user__username=sender_username)
            receiver_catering = CateringCompany.objects.get(user__username=receiver_username)
            Message.objects.create(
                sender=sender_particular.user,  
                receiver=receiver_catering.user,  
                date=timezone.now(),
                content=message_data['content']
            )

def create_catering_services():
    with open('populate/catering_services.json', 'r', encoding='utf-8') as file:
        catering_services_data = json.load(file)
        for service_data in catering_services_data:
            catering_company = CateringCompany.objects.get(user__username=service_data['username'])
            CateringService.objects.create(
                cateringcompany=catering_company,
                name=service_data['name'],
                description=service_data['description'],
                location=service_data['location'],
                capacity=service_data['capacity'],
                price=service_data['price']
            )


def create_menus():
    with open('populate/menus.json', 'r', encoding='utf-8') as file:
        menus_data = json.load(file)

    for company_data in menus_data:
        try:
            company = CateringCompany.objects.get(name=company_data['cateringcompany'])
            service = CateringService.objects.get(name=company_data['cateringservice'], cateringcompany=company)
        except CateringCompany.DoesNotExist:
            print(f"La compañía {company_data['cateringcompany']} no existe en la base de datos.")
            continue
        except CateringService.DoesNotExist:
            print(f"El servicio {company_data['cateringservice']} no existe para la compañía {company_data['cateringcompany']}.")
            continue

        for menu_data in company_data['menus']:
            Menu.objects.create(
                cateringcompany=company,
                cateringservice=service,
                name=menu_data['name'],
                description=menu_data['description'],
                diet_restrictions=menu_data['diet_restrictions']
            )


def create_plates():
    try:
        with open('populate/plates.json', 'r', encoding='utf-8') as file:
            plates_data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    for company_data in plates_data:
        try:
            if 'cateringcompany' not in company_data:
                print("Missing 'cateringcompany' key in data")
                continue

            catering_company = CateringCompany.objects.get(name=company_data['cateringcompany'])
            
            for menu_data in company_data['menus']:
                menu = Menu.objects.get(name=menu_data['menu_name'], cateringcompany=catering_company)
                
                for plate_data in menu_data['plates']:
                    try:
                        Plate.objects.create(
                            cateringcompany=catering_company,
                            menu=menu,
                            name=plate_data['name'],
                            description=plate_data['description'],
                            price=decimal.Decimal(plate_data['price'])
                        )
                    except IntegrityError as e:
                        print(f"Error creating plate: {e}")
        except CateringCompany.DoesNotExist:
            print(f"Catering company {company_data.get('cateringcompany', 'Unknown')} not found in the database")
        except Menu.DoesNotExist:
            print(f"Menu {menu_data.get('menu_name', 'Unknown')} not found for {company_data.get('cateringcompany', 'Unknown')}")
        except KeyError as e:
            print(f"Missing key in menu data: {e}")
           
def create_events():
    with open('populate/events.json', 'r', encoding='utf-8') as file:
        events_data = json.load(file)
        for event_data in events_data:
            catering_company = CateringCompany.objects.get(user__username=event_data['catering_company_username'])
            selected_service = CateringService.objects.get(name=event_data['service_name'], cateringcompany=catering_company)
            particular = Particular.objects.get(user__username=event_data['particular_username'])
            menu = Menu.objects.filter(cateringservice=selected_service).first()  # Omitir si no necesitas asociar menús específicos
            
            Event.objects.create(
                cateringservice=selected_service,
                cateringcompany=catering_company,
                particular=particular,
                menu=menu,
                name=event_data['name'],
                date=datetime.datetime.strptime(event_data['date'], '%Y-%m-%d').date(),
                details=event_data['details'],
                booking_state=event_data['booking_state'],
                number_guests=event_data['number_guests']
            )


reviews_data = [
    {"description": "¡Excelente servicio y comida deliciosa! Definitivamente recomendaré este catering a mis amigos y familiares.", "rating": 5},
    {"description": "La presentación de los platos fue impecable, pero algunos sabores podrían mejorar. En general, una experiencia satisfactoria.", "rating": 4},
    {"description": "¡Increíble! Desde la atención del personal hasta el sabor de los alimentos, todo fue excepcional. Sin duda volveré a contratarlos para futuros eventos.", "rating": 5},
    {"description": "Buena relación calidad-precio, aunque la variedad de opciones en el menú podría ampliarse. El equipo de catering fue amable y profesional.", "rating": 4},
    {"description": "El servicio fue puntual y eficiente, pero algunos invitados expresaron preocupaciones sobre la temperatura de los platos. En general, una experiencia decente.", "rating": 3},
    {"description": "Nos encantaron los postres, ¡fueron el punto destacado del evento! Sin embargo, la comunicación inicial fue un poco confusa. Recomendaría mejorar la coordinación.", "rating": 4},
    {"description": "La comida estuvo deliciosa y bien presentada. Sin embargo, hubo algunos problemas con la disponibilidad de ciertos platos según lo acordado previamente.", "rating": 4},
    {"description": "Los platos principales estaban deliciosos, pero los aperitivos fueron un poco decepcionantes. En general, una experiencia satisfactoria pero con margen de mejora.", "rating": 3},
    {"description": "¡Una experiencia gastronómica excepcional! Los invitados elogiaron la calidad de la comida y el servicio atento del personal. ¡Sin duda volveremos a contratarlos!", "rating": 5},
    {"description": "La comida era deliciosa, pero hubo algunos retrasos en el servicio durante el evento. A pesar de eso, el equipo de catering fue receptivo a nuestras necesidades.", "rating": 3}
]


def create_reviews(num_reviews):
    particulars = Particular.objects.all()
    services = CateringService.objects.all()
    for _ in range(num_reviews):
        Review.objects.create(
            particular=choice(particulars),
            cateringservice=choice(services),
            rating=reviews_data[_]['rating'],
            description=reviews_data[_]['description'],
            date=faker.date_between(start_date='-1y', end_date='today')
        )


def create_employee_work_services():
    # Asegúrate de que la ruta al archivo JSON sea la correcta
    with open('populate/employee_work_services.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        employee = Employee.objects.get(user__username=item['employee'])
        cateringservice = CateringService.objects.get(name=item['cateringservice'])
        event_name = item['event'].split(' (')[0]  # Asumiendo que el evento se guarda sin fecha en la base de datos
        
        try:
            event = Event.objects.get(name=event_name)
            # Crear EmployeeWorkService asegurándose que no hay duplicados para un servicio en curso
            EmployeeWorkService.objects.create(
                employee=employee,
                cateringservice=cateringservice,
                event=event,
                start_date=timezone.datetime.strptime(item['start_date'], '%Y-%m-%d').date(),
                end_date=timezone.datetime.strptime(item['end_date'], '%Y-%m-%d').date(),
                termination_reason=item.get('termination_reason'),
                termination_details=item.get('termination_details', '')
            )
        except Event.MultipleObjectsReturned:
            print(f"Error: Se encontró más de un evento con el nombre '{event_name}'.")
            # Opcionalmente, manejar el error como sea adecuado para la aplicación

# Nota: Asegúrate de tener las importaciones correctas para `timezone` y otros módulos que estés usando.



def create_offers():
    with open('populate/offers.json', 'r', encoding='utf-8') as file:
        offers_data = json.load(file)
        for offer_data in offers_data:
            service = CateringService.objects.get(name=offer_data['service_name'])
            event = Event.objects.get(name=offer_data['event_name'], cateringservice=service)
            
            Offer.objects.create(
                cateringservice=service,
                event=event,
                title=offer_data['title'],
                description=offer_data['description'],
                requirements=offer_data['requirements'],
                location=offer_data['location'],
                start_date=datetime.datetime.strptime(offer_data['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.datetime.strptime(offer_data['end_date'], '%Y-%m-%d').date()
            )

def create_job_applications():
    # Cargar datos desde un archivo JSON
    with open('populate/job_applications.json', 'r', encoding='utf-8') as file:
        job_applications_data = json.load(file)

    for application_data in job_applications_data:
        employee = Employee.objects.get(user__username=application_data['employee_username'])
        offer = Offer.objects.get(title=application_data['offer_title'])

        # Parsear las fechas y hacerlas timezone-aware
        date_application = make_aware(datetime.datetime.strptime(application_data['date_application'], '%Y-%m-%d'))

        # Crear la aplicación de trabajo
        JobApplication.objects.create(
            employee=employee,
            offer=offer,
            date_application=date_application,
            state=application_data['state']
        )

        
recommendation_descriptions = [
    "El empleado demostró una habilidad excepcional para trabajar en equipo, destacándose por su compromiso y dedicación en cada proyecto.",
    "Durante su tiempo con nosotros, el empleado mostró una actitud proactiva y una capacidad innata para resolver problemas de manera eficiente.",
    "Recomiendo encarecidamente al empleado, quien ha demostrado una excelente capacidad de liderazgo y habilidades interpersonales, contribuyendo significativamente al éxito de nuestro equipo.",
    "El desempeño del empleado fue sobresaliente en todas las áreas, mostrando una gran iniciativa y creatividad en la resolución de problemas.",
    "El empleado es altamente confiable y demuestra un alto nivel de integridad en todas sus interacciones profesionales.",
    "Destaco la capacidad del empleado para adaptarse rápidamente a nuevos entornos y desafíos, demostrando una notable flexibilidad y capacidad de aprendizaje.",
    "El empleado es extremadamente eficiente y meticuloso en su trabajo, asegurando siempre la entrega de resultados de alta calidad dentro de los plazos establecidos.",
    "El compromiso del empleado con la excelencia y su constante búsqueda de la mejora continua lo hacen un activo valioso para cualquier equipo.",
    "Durante su tiempo con nosotros, el empleado demostró una ética de trabajo excepcional y una capacidad para superar expectativas en todas las tareas asignadas.",
    "Recomiendo al empleado sin reservas, ya que su actitud positiva y su enfoque orientado a resultados lo convierten en un miembro invaluable de cualquier equipo."
]
        
def create_recommendation_letters(num_recommendations):
    employees = Employee.objects.all()
    caterings = CateringCompany.objects.all()
    for _ in range(num_recommendations):
        employee=choice(employees)
        catering = choice(caterings) 
        description = choice(recommendation_descriptions)
        date = faker.date_this_decade()
        # Crea la carta de recomendación
        RecommendationLetter.objects.create(
            employee=employee,
            catering=catering,
            description=description,
            date=date
    )


def create_task_employee():
    with open('populate/tasks.json', 'r', encoding='utf-8') as file:
        tasks_data = json.load(file)

    for item in tasks_data:
        try:
            with transaction.atomic():
                print(f"Looking for company: {item['cateringcompany']}")
                cateringcompany = CateringCompany.objects.get(user__username=item['cateringcompany'])
                event = Event.objects.get(name=item['event'])
                cateringservice = CateringService.objects.get(name=item['cateringservice'])
                
                task = Task(
                    event=event,
                    cateringservice=cateringservice,
                    cateringcompany=cateringcompany,
                    description=item['description'],
                    assignment_date=timezone.datetime.strptime(item['assignment_date'], '%Y-%m-%d').date(),
                    expiration_date=timezone.datetime.strptime(item['expiration_date'], '%Y-%m-%d').date(),
                    assignment_state=item['assignment_state'],
                    priority=item['priority']
                )
                task.save()

                for username in item['employees']:
                    employee = Employee.objects.get(user__username=username)
                    task.employees.add(employee)

                print(f"Task for {event.name} created and employees assigned successfully.")
        except CateringCompany.DoesNotExist:
            print(f"CateringCompany '{item['cateringcompany']}' does not exist.")
        except Exception as e:
            print(f"Error processing task data: {str(e)}")




def create_superusers():
    superusers_data = [
        {'username': 'admin1', 'email': 'admin1@example.com', 'password': 'admin1'},
        {'username': 'admin2', 'email': 'admin2@example.com', 'password': 'admin2'},
    ]
    for data in superusers_data:
        if not CustomUser.objects.filter(username=data['username']).exists():
            user = CustomUser.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
            user.is_superuser = True
            user.is_staff = True
            user.save()

def populate_database():
    truncate_all_tables()
    create_particulars()
    create_catering_companies()
    create_employees()
    create_messages()
    create_catering_services()
    create_menus()
    create_events()
    create_plates()
    create_reviews(10)
    create_employee_work_services()
    create_offers()
    create_job_applications()
    create_recommendation_letters(10)
    create_task_employee()
    create_superusers()

if __name__ == "__main__":
    populate_database()
    print("Database successfully populated.")