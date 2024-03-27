import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banquetBuddy.settings')
django.setup()
from django.core.files import File
from django.utils import timezone
from faker.providers import person, address
import random
from django.conf import settings
from catering_employees.models import CustomUser, Employee, EnglishLevel, Message
from catering_owners.models import CateringCompany, CateringService, CuisineTypeModel, EmployeeWorkService, Event, JobApplication, Menu, Offer, Plate, Review, Task, TaskEmployee, RecommendationLetter
from catering_particular.models import Particular


from faker import Faker
from core.models import *
from random import randint, choice
faker = Faker(['es_ES'])
faker.add_provider(person)
faker.add_provider(address)

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



preferences = [
    "Comida italiana",
    "Comida mexicana",
    "Comida asiática",
    "Comida vegetariana",
    "Comida vegana",
    "Comida rápida",
    "Comida gourmet",
    "Comida casera",
    "Postres",
    "Bebidas"
]

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


def create_particulars(num_particulars):
    for _ in range(num_particulars):
        user = CustomUser.objects.create_user(username=user_list[_],password = user_list[_], email=user_list[_]+"@gmail.com")
        num_preferences = random.randint(1, 3)
        Particular.objects.create(
            user=user,
            phone_number=faker.phone_number(),
            preferences=random.sample(preferences, num_preferences),
            address=faker.address(),
            is_subscribed=faker.boolean()
        )

catering_names = [
        "DeliciasMediterraneas",
        "SaborOriental",
        "RinconMexicano",
        "GourmetFusion",
        "CocinaAntonio",
        "ExquisitezGastronomica",
        "CateringBenito",
        "SaboresdelMar",
        "SazonCasera",
        "DulcesCaprichos"
    ]

logos_catering = [
    "lamediterranea.jpg",
    "sabororiental.jpg",
    "rinconmexicano.jpg",
    "fusiongourmet.png",
    "cocinaantonio.jpg",
    "mediterranea,jpg",
    "cateringbenito.png"
]

   
catering_descriptions = [
        "Sumérgete en un festín de sabores inspirados en los países bañados por el mar Mediterráneo...",
        "Embárcate en un viaje culinario a través de Asia con nuestra exquisita selección de platos orientales...",
        "Vive la vibrante cultura y los intensos sabores de México con nuestro auténtico menú mexicano...",
        "Explora la innovadora fusión de sabores de nuestra cocina gourmet...",
        "Redescubre los sabores reconfortantes de la cocina tradicional con nuestro menú clásico...",
        "Déjate seducir por la sofisticación y la elegancia de nuestra exquisitez gastronómica...",
        "Embriágate con los aromas y sabores exóticos de Oriente con nuestra deliciosa cocina asiática...",
        "Sumérgete en una experiencia culinaria costera con nuestros deliciosos sabores del mar...",
        "Disfruta del auténtico sabor de la comida casera con nuestro menú reconfortante y familiar...",
        "Déjate seducir por la tentación de nuestros dulces caprichos..."
    ]

    
cuisine_types = [
   ["MEDITERRANEAN"],  
    ["ORIENTAL"],       
    ["MEXICAN"]        
]


def create_catering_companies():
    for i in range(7):
        user = CustomUser.objects.create_user(username=catering_names[i], password=catering_names[i], email=catering_names[i]+"@gmail.com")
        catering_company = CateringCompany.objects.create(
            user=user,
            name=catering_names[i],
            phone_number=faker.phone_number(),
            service_description=catering_descriptions[i],
            logo=None,
            is_verified=faker.boolean(),
            price_plan=choice(['BASE', 'PREMIUM', 'PREMIUM_PRO', 'NO_SUBSCRIBED'])
        )

        # Añadir los tipos de cocina
        for cuisine_key in cuisine_types[i % len(cuisine_types)]:  
            cuisine_instance = CuisineTypeModel.objects.get(type=cuisine_key)
            catering_company.cuisine_types.add(cuisine_instance)

        # logo path
        logo_filename = logos_catering[i]
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
    for _ in range(num_employees):
        user = CustomUser.objects.create_user(username=employee_data[_]['username'], password= employee_data[_]['password'],email=faker.email())
        Employee.objects.create(
            user=user,
            phone_number=faker.phone_number(),
            profession=choice(['Chef', 'Camarero', 'Pastelero']),
            experience=employee_data[_]['experience'],
            skills=employee_data[_]['skill'],
            english_level=employee_data[_]['english_level'],
            location=faker.address(),
            curriculum=None, 
        )


messages_content = [
    "Hola, estamos organizando un evento para celebrar nuestro aniversario de bodas y nos gustaría contratar vuestro servicio de catering. ¿Podrían proporcionarnos más información sobre vuestros menús y precios?",
    "Buenos días, estamos planeando una fiesta de cumpleaños para nuestro hijo y nos gustaría saber si ofrecen opciones de catering para niños. ¿Podrían ayudarnos con esto?",
    "¡Hola! Estamos organizando una conferencia de negocios y necesitamos un servicio de catering para el almuerzo. ¿Podrían proporcionarnos un presupuesto para esto?",
    "Hola, estamos interesados en contratar vuestro servicio de catering para nuestra boda el próximo mes. ¿Podrían decirnos si tienen disponibilidad y cuáles son sus opciones de menú?",
    "Hola, estamos planeando una cena especial para nuestro aniversario y nos gustaría contratar vuestro servicio de catering para la ocasión. ¿Podrían decirnos qué opciones de menú tienen disponibles?",
    "¡Hola! Nos gustaría organizar una fiesta sorpresa para nuestro amigo y nos preguntábamos si podrían ayudarnos con el catering. ¿Podrían proporcionarnos información sobre vuestros servicios y precios?",
    "Hola, estamos organizando un evento benéfico para recaudar fondos y nos gustaría contratar vuestro servicio de catering para la cena. ¿Podrían decirnos si tienen experiencia en eventos de este tipo?",
    "Buenos días, estamos planeando una reunión familiar y nos gustaría contratar vuestro servicio de catering para la comida. ¿Podrían proporcionarnos información sobre vuestras opciones de menú y precios?",
    "Hola, nos gustaría organizar una degustación de vinos en nuestra bodega y estamos buscando un servicio de catering para complementar la experiencia. ¿Podrían ayudarnos con esto?"
]


def create_messages(num_messages):
    users = Particular.objects.all()
    for _ in range(num_messages):
        sender = choice(users)
        receiver = choice(users.exclude(pk=sender.pk))
        Message.objects.create(
            sender=sender.user,  
            receiver=receiver.user,  
            date=timezone.now(),
            content=messages_content[_]
        )

services_name = [
    "Banquete Estelar",
    "Delicias del Chef",
    "Fiesta Gourmet",
    "Cocina de Autor",
    "Buffet Real",
    "Sabor Exclusivo",
    "Eventos Elegantes",
    "Catering Premium",
    "Menús Especiales",
    "Celebración Soñada"
]

services_descriptions = [
    "Experimenta una explosión de sabores con nuestro banquete estelar. Ofrecemos una amplia variedad de platos exquisitos y servicios personalizados para satisfacer tus necesidades.",
    "Las delicias del chef te esperan en cada plato. Nuestro equipo de expertos culinarios se encargará de crear una experiencia gastronómica inolvidable para tu evento.",
    "Haz que tu fiesta sea memorable con nuestro servicio de catering. Desde aperitivos elegantes hasta postres indulgentes, tenemos todo lo que necesitas para impresionar a tus invitados.",
    "Déjanos sorprenderte con nuestra cocina de autor. Cada plato está cuidadosamente diseñado para deleitar tus sentidos y dejar una impresión duradera en tus invitados.",
    "Disfruta de un buffet real con una selección de platos exquisitos de todo el mundo. Nuestro equipo se encargará de cada detalle para que puedas disfrutar de tu evento sin preocupaciones.",
    "Sabor exclusivo es lo que ofrecemos en cada evento. Nuestra pasión por la buena comida se refleja en cada plato que servimos, garantizando una experiencia culinaria excepcional.",
    "Organiza eventos elegantes con nuestro servicio de catering. Desde bodas hasta cenas de gala, nuestro equipo está preparado para hacer realidad tus sueños gastronómicos.",
    "Dale un toque de lujo a tu evento con nuestro catering premium. Desde ingredientes de primera calidad hasta presentaciones elegantes, estamos comprometidos a superar tus expectativas.",
    "Descubre menús especiales diseñados para satisfacer tus gustos más exigentes. Nuestro equipo trabajará contigo para crear una experiencia gastronómica única para tu evento.",
    "Haz realidad la celebración de tus sueños con nuestro servicio de catering. Nos encargaremos de cada detalle para que puedas relajarte y disfrutar junto a tus seres queridos."
]

def create_catering_services(num_services):
    companies = CateringCompany.objects.all()
    for _ in range(num_services):
        CateringService.objects.create(
            cateringcompany=choice(companies),
            name=services_name[_],
            description=services_descriptions[_],
            location=faker.address(),
            capacity=randint(50, 200),
            price=randint(500, 5000) / 100
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

def create_menus(num_menus):
    companies = CateringCompany.objects.all()
    for company in companies:
        for _ in range(num_menus):
            menu = Menu.objects.create(
                cateringcompany=company,
                name=choice(menus_name),
                description=choice(menus_descriptions),
                diet_restrictions=choice(menus_restrictions)
            )

def create_plates():
    plate_images = [
        "plate1.JPG",  
        "plate2.JPG",
        "plate3.JPG",  
        "plate4.JPG",
        "plate5.JPG",  
        "plate6.JPG",
    ]
    for menu in Menu.objects.all():
        num_plates = randint(2, 5)
        for _ in range(num_plates):
            plate_image_filename = choice(plate_images)
            plate_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'plates', plate_image_filename)

            if os.path.exists(plate_image_path):
                with open(plate_image_path, 'rb') as f:
                    try:
                        Plate.objects.create(
                            menu=menu,
                            name=generate_plate_name(),
                            description=generate_plate_description(),
                            price=faker.random_number(digits=2),
                            image=File(f, name=plate_image_filename)
                        )
                    except Exception as e:
                        print(f"Error al crear plato: {e}")
           



def create_events(num_events):
    services = CateringService.objects.all()
    particulars = Particular.objects.all()
    menus = Menu.objects.all()
    for _ in range(num_events):
        menu = choice(menus) if menus else None
        Event.objects.create(
            cateringservice=choice(services),
            particular=choice(particulars),
            menu=menu,
            name=faker.word(),
            date=faker.date_between(start_date='today', end_date='+1y'),
            details=events_details[_],
            booking_state=choice(['CONFIRMED', 'CONTRACT_PENDING', 'CANCELLED','FINALIZED']),
            number_guests=randint(20, 200)
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

def create_tasks(num_tasks):
    events = Event.objects.all()
    services = CateringService.objects.all()
    for _ in range(num_tasks):
        service = choice(services)
        Task.objects.create(
            event=choice(events),
            cateringservice=service,
            cateringcompany=service.cateringcompany,  # Asegúrate de que cada tarea tenga una compañía de catering
            description=tasks_descriptions[_],
            assignment_date=faker.date_between(start_date='-1y', end_date='today'),
            assignment_state=choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            expiration_date=faker.date_between(start_date='today', end_date='+1y'),
            priority=choice(['LOW', 'MEDIUM', 'HIGH'])
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




def generate_plate_name():
    plate_names = ['Ensalada César', 'Tacos al Pastor', 'Paella Valenciana', 'Pasta Carbonara', 'Risotto de Setas', 'Curry de Pollo']
    return choice(plate_names)  # Esto selecciona un nombre de plato al azar de la lista

def generate_plate_description():
    return faker.text(max_nb_chars=200)










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
    for _ in range(num_relations):
        EmployeeWorkService.objects.create(
            employee=choice(employees),
            cateringservice=choice(services)
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
    for _ in range(num_offers):
        Offer.objects.create(
            cateringservice=choice(services),
            title=offers[_]['title'],
            description=offers[_]['description'],
            requirements=offers[_]['requirements'],
            location=offers[_]['location']
        )


def create_job_applications(num_applications):
    employees = Employee.objects.all()
    offers = Offer.objects.all()
    for _ in range(num_applications):
        JobApplication.objects.create(
            employee=choice(employees),
            offer=choice(offers),
            date_application=faker.date_between(start_date='-5d', end_date='today'),
            state=choice(['PENDING', 'IN_REVIEW', 'ACCEPTED'])
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

def populate_database():
    truncate_all_tables()
    create_cuisine_types()  # Crear los tipos de cocina antes de crear las compañías de catering
    create_particulars(8)
    create_catering_companies()
    create_employees(10)
    create_messages(5)
    create_catering_services(10)
    create_menus(10)
    create_events(10)
    create_tasks(10)
    create_plates()
    create_reviews(10)
    create_employee_work_services(10)
    create_offers(10)
    create_job_applications(10)
    create_recommendation_letters(10)

if __name__ == "__main__":
    populate_database()
    print("Database successfully populated.")