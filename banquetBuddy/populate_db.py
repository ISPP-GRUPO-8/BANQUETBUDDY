from datetime import timedelta
import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banquetBuddy.settings')
django.setup()
from django.core.files import File
from django.utils import timezone
from faker.providers import person, address
import random
from django.conf import settings
from catering_employees.models import CustomUser, Employee, Message
from catering_owners.models import CateringCompany, CateringService, CuisineTypeModel, EmployeeWorkService, Event, JobApplication, Menu, Offer, Plate, Review, Task, RecommendationLetter
from catering_particular.models import Particular
from django.contrib.auth import get_user_model
import datetime


from faker import Faker
from core.models import *
from random import randint, choice
from django.utils.timezone import make_aware
faker = Faker(['es_ES'])
faker.add_provider(person)
faker.add_provider(address)
CustomUser = get_user_model()

def create_cuisine_types():
    for cuisine in CuisineType.choices:
        CuisineTypeModel.objects.get_or_create(type=cuisine[0])

create_cuisine_types()


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


events_details = [
    "Una elegante recepción al aire libre en un jardín botánico.",
    "Una cena íntima con vista a la ciudad desde el piso 50 de un rascacielos.",
    "Una fiesta temática con música en vivo y cócteles creativos.",
    "Un buffet de postres para un baby shower de ensueño.",
    "Una degustación de vinos y quesos en una bodega histórica.",
    "Una celebración familiar con juegos y actividades para niños.",
    "Una boda de destino en una playa paradisíaca.",
    "Una cena de gala en un lujoso salón de eventos.",
    "Una inauguración de empresa con catering de comida internacional.",
    "Una fiesta sorpresa con entretenimiento en vivo y baile hasta el amanecer."
]

menus_restrictions = [
    "Sin restricciones: este menú incluye una variedad de platos para todos los gustos y necesidades dietéticas.",
    "Vegetariano: todos los platos de este menú son aptos para vegetarianos, sin carne ni productos de origen animal.",
    "Sin gluten: ideal para personas con intolerancia al gluten, este menú ofrece platos libres de trigo y otros cereales con gluten.",
    "Bajo en calorías: diseñado para aquellos que desean controlar su ingesta de calorías, este menú ofrece opciones saludables y equilibradas.",
    "Sin lactosa: adecuado para personas con intolerancia a la lactosa, este menú excluye productos lácteos de la dieta.",
    "Vegano: todos los platos de este menú son aptos para veganos, sin ingredientes de origen animal.",
    "Orgánico: ingredientes frescos y orgánicos se utilizan en este menú para una experiencia culinaria más saludable y sostenible.",
    "Bajo en carbohidratos: perfecto para aquellos que siguen una dieta baja en carbohidratos, este menú ofrece opciones sin azúcares añadidos ni alimentos ricos en carbohidratos.",
    "Sin frutos secos: ideal para personas con alergias a los frutos secos, este menú excluye cualquier tipo de fruto seco de los platos.",
    "Sin azúcar: diseñado para aquellos que desean reducir su consumo de azúcar, este menú ofrece postres y platos sin azúcares añadidos."
]

def create_menus():
    companies = CateringCompany.objects.all()

    for company in companies:
        available_menu_names = list(menus_name)
        num_menus_to_create = min(len(available_menu_names), random.randint(1, len(available_menu_names)))

        # Obtén todos los servicios de catering de la compañía actual
        company_services = CateringService.objects.filter(cateringcompany=company)

        for _ in range(num_menus_to_create):
            name = choice(available_menu_names)
            available_menu_names.remove(name)

            description = choice(menus_descriptions)
            diet_restrictions = choice(menus_restrictions)

            if company_services:
                # Elige al azar uno de los servicios de catering de esta compañía
                catering_service = choice(company_services)

                Menu.objects.create(
                    cateringcompany=company,
                    cateringservice=catering_service,
                    name=name,
                    description=description,
                    diet_restrictions=diet_restrictions
                )
            else:
                # Si la compañía no tiene servicios de catering, crea el menú sin asociarlo a un servicio específico
                Menu.objects.create(
                    cateringcompany=company,
                    name=name,
                    description=description,
                    diet_restrictions=diet_restrictions
                )


menus_name = [
    "Menú Degustación Mediterráneo",
    "Menú Vegetariano Gourmet",
    "Menú BBQ Americana",
    "Menú Asiático Fusion",
    "Menú Clásico Italiano",
    "Menú Tapas Españolas",
    "Menú Saludable y Equilibrado",
    "Menú Internacional Variado",
    "Menú de Lujo Gourmet",
    "Menú Tradicional de la Abuela"
]

menus_descriptions = [
    "Descubre los sabores del Mediterráneo con este exquisito menú degustación. Desde frescos mariscos hasta platos tradicionales, cada bocado te transportará a la costa del sur de Europa.",
    "Disfruta de una experiencia culinaria sin carne con nuestro menú vegetariano gourmet. Cada plato está cuidadosamente elaborado para resaltar los sabores naturales de los ingredientes frescos y de temporada.",
    "Celebra al estilo estadounidense con nuestro menú BBQ. Desde jugosas hamburguesas hasta costillas ahumadas, este menú es perfecto para una fiesta al aire libre con amigos y familiares.",
    "Embárcate en un viaje culinario por Asia con nuestro menú asiático fusion. Del sushi japonés a los rollitos de primavera vietnamitas, cada plato está inspirado en los sabores y técnicas de cocina de la región.",
    "Viaja a Italia sin salir de tu evento con nuestro menú clásico italiano. Desde la pasta fresca hasta la pizza recién horneada, cada plato te hará sentir como si estuvieras en el corazón de la Toscana.",
    "Disfruta de la variedad y la autenticidad de la cocina española con nuestro menú de tapas. Desde patatas bravas hasta jamón ibérico, cada bocado es una deliciosa explosión de sabor.",
    "Cuida tu bienestar con nuestro menú saludable y equilibrado. Cada plato está diseñado para ofrecer una combinación perfecta de nutrientes y sabor, para que puedas disfrutar de una comida deliciosa sin comprometer tu salud.",
    "Viaja por el mundo con nuestro menú internacional variado. Desde platos tradicionales hasta creaciones innovadoras, este menú ofrece una experiencia culinaria única que satisfará los paladares más exigentes.",
    "Eleva tu evento a otro nivel con nuestro menú de lujo gourmet. Cada plato está elaborado con ingredientes de primera calidad y presentado de manera impecable, para una experiencia gastronómica verdaderamente memorable.",
    "Recupera el sabor de la cocina casera con nuestro menú tradicional de la abuela. Desde platos reconfortantes hasta postres caseros, cada bocado te recordará el hogar y la familia."
]

menus_plates = [
    ["Paella de mariscos", "Ensalada griega", "Pulpo a la gallega", "Pasta al pesto", "Tiramisú"],
    ["Risotto de champiñones", "Tartaleta de espinacas y queso de cabra", "Curry de verduras", "Sushi vegetariano", "Helado de frutas frescas"],
    ["Hamburguesa clásica con papas fritas", "Costillas de cerdo BBQ", "Pollo a la parrilla con salsa barbacoa", "Ensalada de col", "Pie de manzana"],
    ["Sushi variado", "Pad thai de camarones", "Rollitos de primavera con salsa agridulce", "Curry rojo tailandés", "Helado de té verde"],
    ["Spaghetti carbonara", "Pizza margarita", "Lasagna boloñesa", "Ensalada caprese", "Tiramisú"],
    ["Patatas bravas", "Croquetas de jamón", "Gambas al ajillo", "Tortilla española", "Churros con chocolate"],
    ["Ensalada César con pollo a la parrilla", "Salmón al horno con espárragos", "Quinoa con verduras asadas", "Batido de frutas frescas", "Yogur con granola y frutos rojos"],
    ["Sushi nigiri variado", "Curry de pollo indio", "Tacos mexicanos con guacamole", "Pasta carbonara italiana", "Helado de mochi japonés"],
    ["Foie gras con confitura de higos", "Filete de ternera Wagyu", "Langosta a la parrilla con mantequilla de trufa", "Carpaccio de vieiras", "Tarta de chocolate negro con oro comestible"],
    ["Lentejas estofadas", "Estofado de ternera con patatas", "Arroz con leche", "Pastel de manzana", "Galletas de chocolate caseras"]
]

menu_plates_data = {
    "Menú Degustación Mediterráneo": [
        {"name": "Paella de mariscos", "description": "Deliciosa paella con mariscos frescos y arroz aromático."},
        {"name": "Ensalada griega", "description": "Ensalada refrescante con tomate, pepino, aceitunas y queso feta."},
        {"name": "Pulpo a la gallega", "description": "Pulpo tierno cocido a la perfección y sazonado con aceite de oliva y pimentón."},
        {"name": "Pasta al pesto", "description": "Pasta cocida al dente con salsa pesto casera y queso parmesano."},
        {"name": "Tiramisú", "description": "Postre italiano clásico con capas de bizcocho, café y mascarpone."},
    ],
    "Menú Vegetariano Gourmet": [
        {"name": "Risotto de champiñones", "description": "Risotto cremoso con champiñones frescos y queso parmesano."},
        {"name": "Tartaleta de espinacas y queso de cabra", "description": "Tartaleta crujiente rellena de espinacas y queso de cabra."},
        {"name": "Curry de verduras", "description": "Curry aromático con una variedad de verduras frescas y leche de coco."},
        {"name": "Sushi vegetariano", "description": "Variedad de sushi roll con vegetales frescos y arroz sazonado."},
        {"name": "Helado de frutas frescas", "description": "Helado casero con una mezcla de frutas frescas y cremosas."},
    ],
    "Menú BBQ Americana": [
        {"name": "Hamburguesa clásica con papas fritas", "description": "Hamburguesa jugosa con papas fritas crujientes."},
        {"name": "Costillas de cerdo BBQ", "description": "Costillas de cerdo ahumadas y glaseadas con salsa barbacoa."},
        {"name": "Pollo a la parrilla con salsa barbacoa", "description": "Pollo marinado a la parrilla con salsa barbacoa."},
        {"name": "Ensalada de col", "description": "Ensalada fresca de col con aderezo de mayonesa y vinagre."},
        {"name": "Pie de manzana", "description": "Pastel de manzana con una capa crujiente de masa y relleno de manzanas dulces."},
    ],
    "Menú Asiático Fusion": [
        {"name": "Sushi variado", "description": "Variedad de sushi roll con pescado fresco y arroz sazonado."},
        {"name": "Pad thai de camarones", "description": "Plato tailandés de fideos de arroz salteados con camarones y vegetales."},
        {"name": "Rollitos de primavera con salsa agridulce", "description": "Rollitos crujientes rellenos de carne y vegetales, servidos con salsa agridulce."},
        {"name": "Curry rojo tailandés", "description": "Curry picante tailandés con carne o mariscos, leche de coco y especias."},
        {"name": "Helado de té verde", "description": "Helado cremoso con sabor a té verde, un postre refrescante y delicioso."},
    ],
    "Menú Clásico Italiano": [
        {"name": "Spaghetti carbonara", "description": "Spaghetti con salsa carbonara cremosa, panceta y queso parmesano."},
        {"name": "Pizza margarita", "description": "Pizza clásica con salsa de tomate, mozzarella y albahaca fresca."},
        {"name": "Lasagna boloñesa", "description": "Lasagna con capas de pasta, salsa boloñesa y queso derretido."},
        {"name": "Ensalada caprese", "description": "Ensalada italiana con tomate, mozzarella fresca y albahaca."},
        {"name": "Tiramisú", "description": "Postre italiano clásico con capas de bizcocho, café y mascarpone."},
    ],
    "Menú Tapas Españolas": [
        {"name": "Patatas bravas", "description": "Patatas fritas con salsa brava y alioli, un clásico español."},
        {"name": "Croquetas de jamón", "description": "Croquetas cremosas rellenas de jamón y bechamel."},
        {"name": "Gambas al ajillo", "description": "Gambas salteadas en aceite de oliva con ajo y guindilla."},
        {"name": "Tortilla española", "description": "Tortilla de patatas con huevos, patatas y cebolla."},
        {"name": "Churros con chocolate", "description": "Churros crujientes servidos con chocolate caliente para mojar."},
    ],
    "Menú Saludable y Equilibrado": [
        {"name": "Ensalada César con pollo a la parrilla", "description": "Ensalada fresca con pollo a la parrilla, crutones y aderezo César."},
        {"name": "Salmón al horno con espárragos", "description": "Salmón fresco al horno con espárragos y limón."},
        {"name": "Quinoa con verduras asadas", "description": "Quinoa cocida con una variedad de verduras asadas y hierbas."},
        {"name": "Batido de frutas frescas", "description": "Batido cremoso con una mezcla de frutas frescas y yogur."},
        {"name": "Yogur con granola y frutos rojos", "description": "Yogur natural con granola crujiente y frutos rojos."},
    ],
    "Menú Internacional Variado": [
        {"name": "Sushi nigiri variado", "description": "Variedad de nigiri sushi con pescado fresco y arroz sazonado."},
        {"name": "Curry de pollo indio", "description": "Curry picante de pollo con especias indias y arroz basmati."},
        {"name": "Tacos mexicanos con guacamole", "description": "Tacos rellenos de carne, lechuga, tomate, queso y guacamole."},
        {"name": "Pasta carbonara italiana", "description": "Pasta cremosa con salsa de huevo, panceta y queso parmesano."},
        {"name": "Helado de mochi japonés", "description": "Helado japonés envuelto en masa de arroz glutinoso, un postre único y delicioso."},
    ],
    "Menú de Lujo Gourmet": [
        {"name": "Foie gras con confitura de higos", "description": "Foie gras cocido a la perfección con confitura de higos y pan tostado."},
        {"name": "Filete de ternera Wagyu", "description": "Filete de ternera Wagyu asado a la parrilla con una capa dorada y jugosa."},
        {"name": "Langosta a la parrilla con mantequilla de trufa", "description": "Langosta fresca a la parrilla con mantequilla de trufa y limón."},
        {"name": "Carpaccio de vieiras", "description": "Vieiras frescas en láminas finas con aceite de oliva, limón y sal."},
        {"name": "Tarta de chocolate negro con oro comestible", "description": "Tarta de chocolate negro con hojas de oro comestible, un postre lujoso y decadente."},
    ],
    "Menú Tradicional de la Abuela": [
        {"name": "Lentejas estofadas", "description": "Lentejas cocidas a fuego lento con verduras y chorizo, un plato reconfortante."},
        {"name": "Estofado de ternera con patatas", "description": "Ternera estofada con patatas, zanahorias y guisantes, una comida casera clásica."},
        {"name": "Arroz con leche", "description": "Arroz cocido con leche y azúcar, aromatizado con canela y ralladura de limón."},
        {"name": "Pastel de manzana", "description": "Pastel casero con una base de masa crujiente y relleno de manzanas dulces y canela."},
        {"name": "Galletas de chocolate caseras", "description": "Galletas de chocolate crujientes y llenas de sabor, perfectas para un postre o tentempié."},
    ],
}


def generate_plate_name():
    plate_names = ['Ensalada César', 'Tacos al Pastor', 'Paella Valenciana', 'Pasta Carbonara', 'Risotto de Setas', 'Curry de Pollo']
    return choice(plate_names)  # Esto selecciona un nombre de plato al azar de la lista

def generate_plate_description(plate_name):
    descriptions = {
        'Ensalada César': 'Clásica ensalada con lechuga romana, crutones, parmesano y nuestro aderezo César casero.',
        'Tacos al Pastor': 'Sabrosos tacos rellenos de carne al pastor marinada, piña, cebolla y cilantro, servidos con salsa verde.',
        'Paella Valenciana': 'Auténtica paella española con arroz, mariscos frescos, pollo, chorizo y una mezcla de hierbas aromáticas.',
        'Pasta Carbonara': 'Deliciosa pasta con una cremosa salsa carbonara, tocino crujiente, yema de huevo y queso parmesano.',
        'Risotto de Setas': 'Cremoso risotto italiano con una variedad de setas, ajo, vino blanco y queso parmesano.',
        'Curry de Pollo': 'Pollo tierno cocinado en una rica salsa de curry con especias, servido con arroz basmati aromático.'
    }

    # Devuelve la descripción si el nombre del plato se encuentra en el diccionario, de lo contrario, devuelve una descripción genérica
    return descriptions.get(plate_name, 'Delicioso plato preparado con ingredientes frescos y de alta calidad.')


def create_plates():
    for menu_name, plates_data in menu_plates_data.items():
        menus = Menu.objects.filter(name=menu_name)
        for menu in menus:
            cateringcompany = menu.cateringcompany
            for plate_data in plates_data:
                Plate.objects.create(
                    menu=menu,
                    cateringcompany=cateringcompany,
                    name=plate_data["name"],
                    description=plate_data["description"],
                    price=faker.random_number(digits=2)
                )

           
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


tasks_descriptions = [
    "Preparación de menú para evento corporativo.",
    "Coordinación de servicio de catering para boda.",
    "Organización de degustación de platos para evento promocional.",
    "Diseño de menú especializado para cena de gala.",
    "Supervisión de cocina en evento benéfico.",
    "Planificación de servicio de banquetes para conferencia.",
    "Preparación y presentación de platos para sesión de fotos gastronómica.",
    "Gestión de catering para inauguración de local.",
    "Creación de menú temático para fiesta privada.",
    "Coordinación logística para servicio de catering en festival gastronómico."
]


tasks_data = [
    {
        'event_name': 'Fiesta Sorpresa Nocturna',
        'catering_service_name': 'Buffet Real',
        'description': 'Preparación de menú para evento corporativo.',
        'assignment_date': datetime.date(2024, 4, 10),
        'assignment_state': 'PENDING',
        'expiration_date': datetime.date(2024, 5, 10),
        'priority': 'LOW'
    },
    {
        'event_name': 'Fiesta Sorpresa Nocturna',
        'catering_service_name': 'Buffet Real',
        'description': 'Coordinación de servicio de catering para boda.',
        'assignment_date': datetime.date(2024, 4, 10),
        'assignment_state': 'PENDING',
        'expiration_date': datetime.date(2024, 5, 15),
        'priority': 'MEDIUM'
    },
    {
        'event_name': 'Degustación Vinos y Quesos',
        'catering_service_name': 'Buffet Real',
        'description': 'Supervisión de cocina.',
        'assignment_date': datetime.date(2024, 4, 10),
        'assignment_state': 'PENDING',
        'expiration_date': datetime.date(2024, 5, 15),
        'priority': 'MEDIUM'
    },
    # Agrega los otros campos según sea necesario para cada tarea
]

def create_tasks_from_data(tasks_data):
    for task_data in tasks_data:
        try:
            event = Event.objects.get(name=task_data['event_name'])
            catering_service = CateringService.objects.get(name=task_data['catering_service_name'])
            Task.objects.create(
                event=event,
                cateringservice=catering_service,
                cateringcompany=catering_service.cateringcompany,
                description=task_data['description'],
                assignment_date=task_data['assignment_date'],
                assignment_state=task_data['assignment_state'],
                expiration_date=task_data['expiration_date'],
                priority=task_data['priority']
            )
        except (Event.DoesNotExist, CateringService.DoesNotExist) as e:
            print(f"Error: {e}")




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


def create_employee_work_services(num_relations):
    employees = Employee.objects.all()
    services = CateringService.objects.all()
    events = Event.objects.all()
    reasons = [reason.value for reason in TerminationReason]

    if not employees or not services or not events:
        return

    created_relations = set()  # Mantener un registro de las combinaciones creadas

    while len(created_relations) < num_relations:
        employee = choice(employees)
        service = choice(services)
        event = choice(events)

        # Generar fechas de inicio y fin aleatoriamente
        start_date = timezone.now().date() - timedelta(days=random.randint(0, 30))
        end_date = start_date + timedelta(days=random.randint(30, 180))

        # Combinación única
        unique_combination = (employee.user_id if hasattr(employee, 'user_id') else employee.id, service.id, event.id)

        if unique_combination in created_relations:
            continue  # Si la combinación ya existe, intenta de nuevo

        # Verificar superposiciones de fechas para el mismo empleado y servicio
        overlapping = EmployeeWorkService.objects.filter(
            employee=employee,
            cateringservice=service,
            end_date__gte=start_date,
            start_date__lte=end_date
        ).exists()

        if overlapping:
            continue  # Si hay superposición, intenta otra combinación

        # Añadir la combinación a nuestro registro
        created_relations.add(unique_combination)

        # Decidir aleatoriamente si la relación terminará
        terminated = random.choice([True, False])
        termination_reason = random.choice(reasons) if terminated else None

        # Crear la relación EmployeeWorkService
        EmployeeWorkService.objects.create(
            employee=employee,
            cateringservice=service,
            event=event,
            start_date=start_date,
            end_date=end_date if terminated else None,
            termination_reason=termination_reason
        )


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



def create_cuisine_types():
    for cuisine in CuisineType.choices:
        CuisineTypeModel.objects.get_or_create(type=cuisine[0])
        
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
    employees = list(Employee.objects.all())
    tasks = list(Task.objects.all())

    if employees and tasks:
        for t in tasks:
            random_employee = random.choice(employees)
            t.employees.add(random_employee)
            t.save()
            employees.remove(random_employee)


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
    create_cuisine_types()  # Crear los tipos de cocina antes de crear las compañías de catering
    create_particulars()
    create_catering_companies()
    create_employees()
    create_messages()
    create_catering_services()
    create_menus()
    create_events()
    create_tasks_from_data(tasks_data)
    create_plates()
    create_reviews(10)
    create_employee_work_services(100)
    create_offers()
    create_job_applications()
    create_recommendation_letters(10)
    create_task_employee()
    create_superusers()

if __name__ == "__main__":
    populate_database()
    print("Database successfully populated.")