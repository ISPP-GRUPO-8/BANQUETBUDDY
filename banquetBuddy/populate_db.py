from datetime import timedelta
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



user_list =[
    'Pablo',
    'Juan',
    'Antonio',
    'David',
    'Manuel',
    'Jaime',
    'Luis',
    'Mateo',
]

phone_numbers = [
    '555-1234',
    '555-5678',
    '555-9012',
    '555-3456',
    '555-7890',
    '555-2345',
    '555-6789',
    '555-0123',
]

addresses = [
    '123 Calle Principal',
    '456 Avenida Central',
    '789 Paseo de la Montaña',
    '101 Ruta del Sol',
    '202 Camino Real',
    '303 Boulevard Norte',
    '404 Carrera Sur',
    '505 Callejón Este',
]

preferences_per_user = [
    ["Comida italiana", "Comida vegetariana", "Postres"],
    ["Comida mexicana", "Comida rápida"],
    ["Comida asiática", "Comida vegana", "Bebidas"],
    ["Comida italiana", "Comida casera"],
    ["Comida rápida", "Postres"],
    ["Comida vegetariana", "Bebidas"],
    ["Comida gourmet", "Comida casera"],
    ["Comida mexicana", "Comida vegana", "Comida rápida"],
]

def create_particulars(num_particulars):
    for i in range(num_particulars):
        user = CustomUser.objects.create_user(username=user_list[i], password=user_list[i], email=user_list[i]+"@gmail.com")
        Particular.objects.create(
            user=user,
            phone_number=phone_numbers[i],
            preferences=preferences_per_user[i],
            address=addresses[i],
            is_subscribed=True  # Cambié esto a True, ya que parece que quieres que todos estén suscritos
        )


catering_data = [
    {
        'username': 'DeliciasMediterraneas',
        'password': 'DeliciasMediterraneas',
        'name': 'Delicias Mediterráneas',
        'service_description':         "Sumérgete en un festín de sabores inspirados en los países bañados por el mar Mediterráneo...",
        'logo':'lamediterranea.jpg',
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM_PRO'
    },
    {
        'username': 'SaborOriental',
        'password': 'SaborOriental',
        'name': 'Sabor Oriental',
        'service_description': "Embárcate en un viaje culinario a través de Asia con nuestra exquisita selección de platos orientales...",
        'logo': 'sabororiental.jpg',
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'RinconMexicano',
        'password': 'RinconMexicano',
        'name': 'Rincón Mexicano',
        'service_description': "Vive la vibrante cultura y los intensos sabores de México con nuestro auténtico menú mexicano...",
        'logo': 'rinconmexicano.jpg',
        'phone_number': faker.phone_number(),
        'is_verified': 'False',
        'price_plan': 'NO_SUSCRIBED'
    },
    {
        'username': 'GourmetFusion',
        'password': 'GourmetFusion',
        'name': 'Gourmet Fusion',
        'service_description': "Explora la innovadora fusión de sabores de nuestra cocina gourmet...",
        'logo': 'fusiongourmet.png',
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'CocinaAntonio',
        'password': 'CocinaAntonio',
        'name': 'Cocina Antonio',
        'service_description': "Redescubre los sabores reconfortantes de la cocina tradicional con nuestro menú clásico...",
        'logo': 'cocinaantonio.jpg',
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'ExquisitezGastronomica',
        'password': 'ExquisitezGastronomica',
        'name': 'Exquisitez Gastronómica',
        'service_description': "Déjate seducir por la sofisticación y la elegancia de nuestra exquisitez gastronómica...",
        'logo': 'mediterranea.jpg',
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'CateringBenito',
        'password': 'CateringBenito',
        'name': 'Catering Benito',
        'service_description': "Embriágate con los aromas y sabores exóticos de Oriente con nuestra deliciosa cocina asiática...",
        'logo': 'cateringbenito.png',
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'SaboresdelMar',
        'password': 'SaboresdelMar',
        'name': 'Sabores del Mar',
        'service_description': "Sumérgete en una experiencia culinaria costera con nuestros deliciosos sabores del mar...",
        'logo': '',  # Aquí puedes proporcionar el nombre del archivo de logo si lo tienes
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'SazonCasera',
        'password': 'SazonCasera',
        'name': 'Sazón Casera',
        'service_description': "Disfruta del auténtico sabor de la comida casera con nuestro menú reconfortante y familiar...",
        'logo': '',  # Aquí puedes proporcionar el nombre del archivo de logo si lo tienes
        'phone_number': faker.phone_number(),
        'is_verified': 'True',
        'price_plan': 'PREMIUM'
    },
    {
        'username': 'DulcesCaprichos',
        'password': 'DulcesCaprichos',
        'name': 'Dulces Caprichos',
        'service_description': "Déjate seducir por la tentación de nuestros dulces caprichos...",
        'logo': '',  # Aquí puedes proporcionar el nombre del archivo de logo si lo tienes
        'phone_number': faker.phone_number(),
        'is_verified': 'False',
        'price_plan': 'PREMIUM'
    }
]

cuisine_types = [
   ["MEDITERRANEAN"],  
    ["ORIENTAL"],       
    ["MEXICAN"]        
]


def create_catering_companies():
    for i, catering_info in enumerate(catering_data):
        user = CustomUser.objects.create_user(username=catering_info['username'], password=catering_info['password'], email=catering_info['username'] + "@gmail.com")
        catering_company = CateringCompany.objects.create(
            user=user,
            name=catering_info['name'],
            phone_number=catering_info['phone_number'],
            service_description=catering_info['service_description'],
            is_verified=catering_info['is_verified'],
            price_plan=catering_info['price_plan']
        )

        # Añadir los tipos de cocina
        for cuisine_type in cuisine_types[i % len(cuisine_types)]:  
            cuisine_instance = CuisineTypeModel.objects.get_or_create(type=cuisine_type)[0]
            catering_company.cuisine_types.add(cuisine_instance)

        # Añadir el logo si está disponible
        logo_filename = catering_info.get('logo', None)
        if logo_filename:
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logos', logo_filename)
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    catering_company.logo = File(f, name=logo_filename)
                    catering_company.save()

employee_data = [
    {
        'username': 'OliverS',
        'password': 'employee1',
        'experience': 'Experiencia en la preparación de banquetes para grandes eventos',
        'skill': 'Creatividad para desarrollar platos innovadores',
        'english_level': 'C1'
    },
    {
        'username': 'WillJ98',
        'password': 'employee2',
        'experience': 'Trabajo en restaurantes de cocina internacional',
        'skill': 'Trabajo en equipo en entornos de alta presión',
        'english_level': 'B2'
    },
    {
        'username': 'HarryB_22',
        'password': 'employee3',
        'experience': 'Gestión de la logística de eventos gastronómicos',
        'skill': 'Destreza en la decoración y presentación de platos',
        'english_level': 'A2'
    },
    {
        'username': 'GeorgeM_10',
        'password': 'employee4',
        'experience': 'Supervisión de personal en servicios de catering',
        'skill': 'Habilidad para adaptarse a las preferencias y restricciones dietéticas de los clientes',
        'english_level': 'NONE'
    },
    {
        'username': 'JackW',
        'password': 'employee5',
        'experience': 'Planificación y ejecución de menús para eventos especiales',
        'skill': 'Comunicación efectiva con clientes y proveedores',
        'english_level': 'C2'
    },
    {
        'username': 'AmeliaW',
        'password': 'employee6',
        'experience': 'Experiencia en la gestión de cocinas industriales',
        'skill': 'Gestión del tiempo para coordinar la preparación de múltiples platos',
        'english_level': 'C1'
    },
    {
        'username': 'OliviaT',
        'password': 'employee7',
        'experience': 'Conocimiento de normativas de higiene y seguridad alimentaria',
        'skill': 'Capacidad para resolver problemas rápidamente durante eventos en vivo',
        'english_level': 'B1'
    },
    {
        'username': 'IsabellaG',
        'password': 'employee8',
        'experience': 'Trabajo en servicios de catering para bodas y eventos sociales',
        'skill': 'Conocimiento de técnicas de servicio y atención al cliente',
        'english_level': 'A1'
    },
    {
        'username': 'AvaJ',
        'password': 'employee9',
        'experience': 'Participación en catas y maridajes de vinos y alimentos',
        'skill': 'Flexibilidad para ajustarse a cambios de último minuto en los pedidos',
        'english_level': 'C1'
    },
    {
        'username': 'SophiaM99',
        'password': 'employee10',
        'experience': 'Manejo de equipos y utensilios especializados en cocina',
        'skill': 'Compromiso con la calidad y la excelencia en la cocina',
        'english_level': 'C1'
    }
]


def create_employees(num_employees):
    for i in range(num_employees):
        user = CustomUser.objects.create_user(username=employee_data[i]['username'], password= employee_data[i]['password'],email=employee_data[i]['username'] + "@gmail.com")
        employee = Employee.objects.create(
            user=user,
            phone_number=faker.phone_number(),
            profession=choice(['Chef', 'Camarero', 'Pastelero']),
            experience=employee_data[i]['experience'],
            skills=employee_data[i]['skill'],
            english_level=employee_data[i]['english_level'],
            location=faker.address(),
            curriculum=None
        )
        
        curriculum_filename = 'curriculum.pdf'
        curriculum_path = os.path.join(settings.MEDIA_ROOT, 'curriculums', curriculum_filename)
        
        if os.path.exists(curriculum_path):
            with open(curriculum_path, 'rb') as f:
                employee.curriculum = File(f, name=curriculum_filename)
                employee.save()


messages_content = [
    {
        'content': "Hola, estamos organizando un evento para celebrar nuestro aniversario de bodas y nos gustaría contratar vuestro servicio de catering. ¿Podrían proporcionarnos más información sobre vuestros menús y precios?",
        'sender': 'Pablo',
        'receiver': 'DeliciasMediterraneas'
    },
    {
        'content': "Buenos días, estamos planeando una fiesta de cumpleaños para nuestro hijo y nos gustaría saber si ofrecen opciones de catering para niños. ¿Podrían ayudarnos con esto?",
        'sender': 'Juan',
        'receiver': 'SaborOriental'
    },
    {
        'content': "¡Hola! Estamos organizando una conferencia de negocios y necesitamos un servicio de catering para el almuerzo. ¿Podrían proporcionarnos un presupuesto para esto?",
        'sender': 'Antonio',
        'receiver': 'GourmetFusion'
    },
    {
        'content': "Hola, estamos interesados en contratar vuestro servicio de catering para nuestra boda el próximo mes. ¿Podrían decirnos si tienen disponibilidad y cuáles son sus opciones de menú?",
        'sender': 'David',
        'receiver': 'CocinaAntonio'
    },
    {
        'content': "Hola, estamos planeando una cena especial para nuestro aniversario y nos gustaría contratar vuestro servicio de catering para la ocasión. ¿Podrían decirnos qué opciones de menú tienen disponibles?",
        'sender': 'Manuel',
        'receiver': 'ExquisitezGastronomica'
    },
    {
        'content': "¡Hola! Nos gustaría organizar una fiesta sorpresa para nuestro amigo y nos preguntábamos si podrían ayudarnos con el catering. ¿Podrían proporcionarnos información sobre vuestros servicios y precios?",
        'sender': 'Jaime',
        'receiver': 'CateringBenito'
    },
    {
        'content': "Hola, estamos organizando un evento benéfico para recaudar fondos y nos gustaría contratar vuestro servicio de catering para la cena. ¿Podrían decirnos si tienen experiencia en eventos de este tipo?",
        'sender': 'Luis',
        'receiver': 'SaboresdelMar'
    },
    {
        'content': "Buenos días, estamos planeando una reunión familiar y nos gustaría contratar vuestro servicio de catering para la comida. ¿Podrían proporcionarnos información sobre vuestras opciones de menú y precios?",
        'sender': 'Mateo',
        'receiver': 'SazonCasera'
    },
    {
        'content': "Hola, nos gustaría organizar una degustación de vinos en nuestra bodega y estamos buscando un servicio de catering para complementar la experiencia. ¿Podrían ayudarnos con esto?",
        'sender': 'Pablo',
        'receiver': 'DulcesCaprichos'
    }
]


def create_messages(num_messages):
    users = Particular.objects.all()
    for _ in range(num_messages):
        message_data = messages_content[_]
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




catering_services_data = [
    {
        'username': 'DeliciasMediterraneas',
        'name': "Banquete Estelar",
        'description': "Experimenta una explosión de sabores con nuestro banquete estelar. Ofrecemos una amplia variedad de platos exquisitos y servicios personalizados para satisfacer tus necesidades.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'SaborOriental',
        'name': "Delicias del Chef",
        'description': "Las delicias del chef te esperan en cada plato. Nuestro equipo de expertos culinarios se encargará de crear una experiencia gastronómica inolvidable para tu evento.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'GourmetFusion',
        'name': "Fiesta Gourmet",
        'description': "Haz que tu fiesta sea memorable con nuestro servicio de catering. Desde aperitivos elegantes hasta postres indulgentes, tenemos todo lo que necesitas para impresionar a tus invitados.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'DeliciasMediterraneas',
        'name': "Cocina de Autor",
        'description': "Déjanos sorprenderte con nuestra cocina de autor. Cada plato está cuidadosamente diseñado para deleitar tus sentidos y dejar una impresión duradera en tus invitados.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'CocinaAntonio',
        'name': "Buffet Real",
        'description': "Disfruta de un buffet real con una selección de platos exquisitos de todo el mundo. Nuestro equipo se encargará de cada detalle para que puedas disfrutar de tu evento sin preocupaciones.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'ExquisitezGastronomica',
        'name': "Sabor Exclusivo",
        'description': "Sabor exclusivo es lo que ofrecemos en cada evento. Nuestra pasión por la buena comida se refleja en cada plato que servimos, garantizando una experiencia culinaria excepcional.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'DeliciasMediterraneas',
        'name': "Eventos Elegantes",
        'description': "Organiza eventos elegantes con nuestro servicio de catering. Desde bodas hasta cenas de gala, nuestro equipo está preparado para hacer realidad tus sueños gastronómicos.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'SaboresdelMar',
        'name': "Catering Premium",
        'description': "Dale un toque de lujo a tu evento con nuestro catering premium. Desde ingredientes de primera calidad hasta presentaciones elegantes, estamos comprometidos a superar tus expectativas.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'SazonCasera',
        'name': "Menús Especiales",
        'description': "Descubre menús especiales diseñados para satisfacer tus gustos más exigentes. Nuestro equipo trabajará contigo para crear una experiencia gastronómica única para tu evento.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    },
    {
        'username': 'DulcesCaprichos',
        'name': "Celebración Soñada",
        'description': "Haz realidad la celebración de tus sueños con nuestro servicio de catering. Nos encargaremos de cada detalle para que puedas relajarte y disfrutar junto a tus seres queridos.",
        'location': faker.address(),
        'capacity': randint(50, 200),
        'price': randint(500, 5000) / 100
    }
]

def create_catering_services(num_services):
    for i in range(num_services):
        service_data = catering_services_data[i]
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

           



event_names = [
    "Recepción Jardín Botánico",
    "Cena Panorámica Urbana",
    "Fiesta Temática Musical",
    "Buffet Dulces Sueños",
    "Degustación Vinos y Quesos",
    "Celebración Familiar Divertida",
    "Boda Playa Paradisíaca",
    "Cena de Gala Elegante",
    "Inauguración Empresarial Internacional",
    "Fiesta Sorpresa Nocturna"
]

event_data_list = [
    {
        'name': 'Recepción Jardín Botánico',
        'date': datetime.date(2024, 4, 28),
        'details': "Celebre su evento en un entorno natural único. Nuestra recepción en el Jardín Botánico ofrece un ambiente sereno y elegante, perfecto para cualquier ocasión especial.",
        'booking_state': 'CONFIRMED',
        'number_guests': 120,
        'particular_username': 'Pablo',
        'service': 'Banquete Estelar',   # Nombre de usuario del particular asociado
        # Otros campos según sea necesario
    },
    {
        'name': 'Cena Panorámica Urbana',
        'date': datetime.date(2024, 5, 20),
        'details': "Disfrute de una vista impresionante de la ciudad mientras saborea una deliciosa cena con nuestros platos exclusivos. Una experiencia gastronómica inolvidable en lo alto de la urbe.",
        'booking_state': 'CONFIRMED',
        'number_guests': 80,
        'particular_username': 'Jaime', 
        'service': 'Banquete Estelar', # Nombre de usuario del particular asociado
        # Otros campos según sea necesario
    },
    {
        'name': 'Fiesta Temática Musical',
        'date': datetime.date(2024, 6, 10),
        'details': "¡Que suene la música! Organice una fiesta temática musical con nosotros y déjese llevar por los ritmos más pegajosos. Nuestro equipo se encargará de crear una atmósfera vibrante y llena de energía.",
        'booking_state': 'CONFIRMED',
        'number_guests': 150,
        'particular_username': 'Pablo',
        'service': 'Delicias del Chef',
        # Otros campos según sea necesario
    },
    {
        'name': 'Buffet Dulces Sueños',
        'date': datetime.date(2024, 7, 5),
        'details': "Deléitese con una variedad de postres exquisitos en nuestro buffet de dulces sueños. Desde tartas caseras hasta macarons gourmet, tenemos algo para satisfacer todos los antojos.",
        'booking_state': 'CONTRACT_PENDING',
        'number_guests': 100,
        'particular_username': 'David',
        'service': 'Buffet Real',
        # Otros campos según sea necesario
    },
    {
        'name': 'Degustación Vinos y Quesos',
        'date': datetime.date(2024, 5, 15),
        'details': "Descubre los mejores maridajes de vinos y quesos en nuestra degustación especial. Únete a nosotros para una experiencia sensorial única llena de sabores y aromas.",
        'booking_state': 'CONTRACT_PENDING',
        'number_guests': 50,
        'particular_username': 'Manuel',
        'service': 'Buffet Real',
        # Otros campos según sea necesario
    },
    {
        'name': 'Celebración Familiar Divertida',
        'date': datetime.date(2024, 5, 20),
        'details': "Celebre momentos especiales en familia con nuestra celebración familiar divertida. Ofrecemos entretenimiento para todas las edades y una variedad de platos deliciosos para disfrutar juntos.",
        'booking_state': 'CANCELLED',
        'number_guests': 80,
        'particular_username': 'Juan',
        'service': 'Catering Premium',
        # Otros campos según sea necesario
    },
    {
        'name': 'Boda Playa Paradisíaca',
        'date': datetime.date(2024, 4, 8),
        'details': "Haga realidad su sueño de una boda en la playa con nosotros. Con nuestras impresionantes vistas y servicios de catering excepcionales, su día especial será inolvidable.",
        'booking_state': 'FINALIZED',
        'number_guests': 200,
        'particular_username': 'Pablo',
        'service': 'Cocina de Autor',
        # Otros campos según sea necesario
    },
    {
        'name': 'Cena de Gala Elegante',
        'date': datetime.date(2024, 5, 12),
        'details': "Disfrute de una noche de elegancia y sofisticación en nuestra cena de gala. Con un menú exquisito y un ambiente refinado, le garantizamos una experiencia inolvidable.",
        'booking_state': 'CONFIRMED',
        'number_guests': 150,
        'particular_username': 'Manuel',
        'service': 'Eventos Elegantes',
        # Otros campos según sea necesario
    },
    {
        'name': 'Inauguración Empresarial Internacional',
        'date': datetime.date(2024, 5, 25),
        'details': "Celebre la apertura de su empresa con un evento inolvidable. Nuestro servicio de catering internacional hará que su inauguración sea un éxito en todo el mundo.",
        'booking_state': 'CONTRACT_PENDING',
        'number_guests': 300,
        'particular_username': 'David',
        'service': 'Fiesta Gourmet',
        # Otros campos según sea necesario
    },
    {
        'name': 'Fiesta Sorpresa Nocturna',
        'date': datetime.date(2024, 5, 10),
        'details': "Sorprende a tus seres queridos con una fiesta sorpresa nocturna. Nuestro equipo se encargará de todos los detalles para que puedas disfrutar de una velada llena de diversión y emoción.",
        'booking_state': 'CONFIRMED',
        'number_guests': 50,
        'particular_username': 'Juan',
        'service': 'Buffet Real',
        # Otros campos según sea necesario
    },
    # Agrega el resto de eventos con sus respectivos datos
]

def create_events():
    for event_data in event_data_list:
        particulars = Particular.objects.all()
        menus = Menu.objects.all()

        menu = choice(menus) if menus else None
        selected_service = CateringService.objects.get(name=event_data['service'])
        particular = particulars.get(user__username=event_data['particular_username'])

        Event.objects.create(
            cateringservice=selected_service,
            cateringcompany=selected_service.cateringcompany,
            particular=particular,
            menu=menu,
            name=event_data['name'],
            date=event_data['date'],
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
        'event_name': 'Degustación Vinos y Quesos',
        'catering_service_name': 'Buffet Real',
        'description': 'Coordinación de servicio de catering para boda.',
        'assignment_date': datetime.date(2024, 4, 10),
        'assignment_state': 'IN_PROGRESS',
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

    if not employees or not services or not events:
        return

    for _ in range(num_relations):
        employee = choice(employees)
        service = choice(services)
        event = choice(events)  # Seleccionar un evento al azar

        # Generar fechas de inicio y fin de manera aleatoria
        start_date = timezone.now().date() - timedelta(days=random.randint(0, 30))
        end_date = start_date + timedelta(days=random.randint(30, 180))

        # Verificar si existe una superposición de fechas
        overlapping_assignments = EmployeeWorkService.objects.filter(
            employee=employee,
            cateringservice=service,
            event=event,  # Asegúrate de incluir el evento en la consulta
            end_date__gte=start_date,
            start_date__lte=end_date
        )

        # Si no hay superposición, crear la asignación
        if not overlapping_assignments.exists():
            EmployeeWorkService.objects.create(
                employee=employee,
                cateringservice=service,
                event=event,  # Asignar el evento
                start_date=start_date,
                end_date=end_date
            )




offers = [
    {
        "title": "Oferta especial de primavera",
        "description": "¡Celebre la llegada de la primavera con nuestros deliciosos menús de temporada! Desde platos frescos y ligeros hasta opciones más sustanciales, tenemos todo lo que necesita para hacer de su evento un éxito.",
        "requirements": "Experiencia previa en catering y disponibilidad para eventos durante el día.",
        "location": "Ciudad Jardín, Calle Flores 123"
    },
    {
        "title": "Promoción de verano: BBQ Party",
        "description": "¡Disfrute del sol y del aire libre con nuestra promoción especial de verano! Organice una barbacoa en su jardín o terraza y déjese llevar por nuestros deliciosos platos a la parrilla.",
        "requirements": "Habilidades culinarias en cocina al aire libre y disponibilidad para fines de semana y días festivos.",
        "location": "Playa del Sol, Avenida Marítima 456"
    },
    {
        "title": "Oferta de otoño: Menú de cosecha",
        "description": "¡Celebre la temporada de cosecha con nuestro menú especial de otoño! Ingredientes frescos y de temporada se combinan para ofrecer una experiencia culinaria única que deleitará a sus invitados.",
        "requirements": "Conocimientos en cocina de temporada y disponibilidad para eventos de noche.",
        "location": "Pueblo Viejo, Plaza Principal 789"
    },
    {
        "title": "Promoción de invierno: Cena de Navidad",
        "description": "¡Deleite a sus seres queridos con una deliciosa cena de Navidad preparada por nuestros talentosos chefs! Desde platos tradicionales hasta opciones modernas, tenemos todo lo necesario para hacer de su celebración una experiencia inolvidable.",
        "requirements": "Experiencia previa en eventos festivos y disponibilidad para fines de semana y días festivos.",
        "location": "Villa Invierno, Calle Nieve 101"
    },
    {
        "title": "Oferta corporativa: Almuerzos de negocios",
        "description": "¡Impresione a sus clientes y empleados con nuestros exquisitos almuerzos de negocios! Menús personalizados y servicio profesional garantizan el éxito de sus reuniones y eventos corporativos.",
        "requirements": "Habilidades de presentación de alimentos y disponibilidad para eventos durante la semana.",
        "location": "Centro Empresarial, Calle Negocios 222"
    },
    {
        "title": "Promoción de cumpleaños: Fiesta temática",
        "description": "¡Celebre su cumpleaños de una manera única con nuestra fiesta temática personalizada! Desde la decoración hasta el menú, nos encargamos de todos los detalles para que pueda disfrutar de su día especial sin preocupaciones.",
        "requirements": "Creatividad en diseño de eventos y disponibilidad para fines de semana.",
        "location": "Barrio Feliz, Calle Fiesta 333"
    },
    {
        "title": "Oferta familiar: Cena de domingo",
        "description": "¡Reúna a su familia para una deliciosa cena de domingo sin tener que preocuparse por cocinar! Nuestros menús familiares ofrecen una variedad de platos para satisfacer los gustos de todos.",
        "requirements": "Experiencia en cocina familiar y disponibilidad para eventos de tarde.",
        "location": "Colina Verde, Calle Familia 444"
    },
    {
        "title": "Promoción de aniversario: Banquete elegante",
        "description": "¡Celebre su aniversario con un banquete elegante diseñado para impresionar! Desde la recepción hasta el postre, nos aseguramos de que cada detalle sea perfecto para su ocasión especial.",
        "requirements": "Experiencia en eventos formales y disponibilidad para fines de semana y eventos nocturnos.",
        "location": "Avenida Elegancia, Salón Magnífico 555"
    },
    {
        "title": "Oferta de inauguración: Brunch de bienvenida",
        "description": "¡Dale la bienvenida a tus invitados con un brunch de inauguración inolvidable! Desde platos salados hasta opciones dulces, nuestro brunch ofrece algo para todos los gustos.",
        "requirements": "Conocimientos en cocina para eventos de inauguración y disponibilidad para eventos durante el día.",
        "location": "Barrio Nuevo, Calle Bienvenida 666"
    },
    {
        "title": "Promoción de fiesta de fin de año",
        "description": "¡Celebra el fin de año con una fiesta espectacular y un menú especial para despedir el año viejo y dar la bienvenida al nuevo! Música, comida y diversión aseguradas para una noche inolvidable.",
        "requirements": "Experiencia en eventos festivos y disponibilidad para eventos nocturnos.",
        "location": "Plaza Fiesta, Calle Año Nuevo 777"
    }
]

def create_offers(num_offers):
    services = CateringService.objects.all()
    events = Event.objects.filter(booking_state='CONFIRMED')  # Asegúrate de elegir solo eventos confirmados si es necesario

    for i in range(num_offers):
        if not services or not events:
            break

        service = choice(services)
        event = choice(events)  # Elegir un evento al azar

        # Generar fechas de inicio y fin de manera aleatoria
        start_date = timezone.now().date() + timedelta(days=random.randint(1, 30))  # Fecha de inicio en el futuro
        end_date = start_date + timedelta(days=random.randint(30, 180))  # Fecha de fin después de la fecha de inicio

        Offer.objects.create(
            cateringservice=service,
            event=event,  # Asignar el evento seleccionado
            title=offers[i]['title'],
            description=offers[i]['description'],
            requirements=offers[i]['requirements'],
            location=offers[i]['location'],
            start_date=start_date,
            end_date=end_date
        )


# def create_job_applications(num_applications):
#     employees = Employee.objects.all()
#     offers = Offer.objects.all()
#     for _ in range(num_applications):
#         JobApplication.objects.create(
#             employee=choice(employees),
#             offer=choice(offers),
#             date_application=faker.date_between(start_date='-5d', end_date='today'),
#             state=choice(['PENDING', 'REJECTED', 'ACCEPTED'])
#         )



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
    create_particulars(8)
    create_catering_companies()
    create_employees(10)
    create_messages(5)
    create_catering_services(10)
    create_menus()
    create_events()
    create_tasks_from_data(tasks_data)
    create_plates()
    create_reviews(10)
    create_employee_work_services(100)
    create_offers(10)
    # create_job_applications(10)
    create_recommendation_letters(10)
    create_task_employee()
    create_superusers()

if __name__ == "__main__":
    populate_database()
    print("Database successfully populated.")