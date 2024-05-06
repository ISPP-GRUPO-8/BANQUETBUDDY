
Universidad de Sevilla
Escuela Técnica Superior de Ingeniería Informática

Sprint 3

BanquetBuddy

**Reviewer’s Guide**



Grado en Ingeniería Informática – Ingeniería del Software
Ingeniería del Software y Práctica Profesional

Curso 2023 – 2024

|**Fecha**|**Versión**|
| :-: | :-: |
|01/04/2024|1\.0|
|22/04/2024|1\.1|
|05/05/2024|1\.2|


|**Grupo de prácticas:  8**|**Tipo de contribución**|
| :-: | :-: |
|Mario Sánchez Naranjo|Actualización del documento para la preparación del lanzamiento del proyecto(Autor,revisor)|

#






<a name="_u5a107hff4x7"></a>**Índice de contenido**

[1.Introducción	4](#_oz6624syu5h)

[2. Funcionalidades	4](#_l5rufmenkmpv)

[2.1 Funcionalidades Comunes	4](#_9tzh197xg91q)

[Login	4](#_ppjupmxb1smo)

[Reseteo de contraseña	4](#_w0hmy96ip0jq)

[Elección de registro	5](#_o0tko6m8t3ee)

[Pasarela de pago	6](#_ho9pg87nz5ot)

[About-us	6](#_yv8dtss3x9yq)

[Información de contacto	7](#_wyu22ssat45b)

[Preguntas frecuentes	7](#_xhrhf7rfjizs)

[Política de privacidad	8](#_lq2dsae3jwqb)

[Términos y condiciones	8](#_hh6bn2gg4qh3)

[Reporte de errores	9](#_lpfvrsweir3b)

[2.2 Funcionalidad de Catering	10](#_3b62aqvwzr4o)

[Registro Catering	10](#_77lcq0wkonlj)

[Listado de menús	11](#_ca1ocx5uvfjn)

[Añadir menú	11](#_5js8edq8opex)

[Editar Menú	13](#_6b0zazo2qm0p)

[Borrar Menu	13](#_uuqsbtigzq20)

[Perfil de catering	14](#_n4699b99ajke)

[Editar perfil de catering	14](#_c5vtmluj1vw9)

[Planes de subscripción	15](#_nw1bdciusw4y)

[Gestión de Servicios	16](#_mcqrc236si8m)

[Carta de recomendación a empleados	19](#_1604n6misfbp)

[Listado de platos	19](#_oh44tx1luzz7)

[Crear nuevo plato	20](#_wbkt9afcptdz)

[Editar plato	21](#_5ct3xn1kgxpm)

[Eliminar plato	21](#_ibhlknq5qllp)

[Listado de ofertas publicadas	22](#_wda1vzgh4js9)

[Contratación de empleo(CORE)	22](#_okrob04e0q4v)

[Editar oferta	26](#_3wmhw0dtele5)

[Borrar oferta	26](#_3mqnh8r4zycj)

[Listado de empleados que han aplicado una oferta	27](#_etlkdp80xxi0)

[Reservas	27](#_brd9129g2jrq)

[Calendario: elección de servicio	28](#_cwl6dsfobgw8)

[Calendario	28](#_8equoco94nuq)

[Gestión de tareas(PREMIUM)	29](#_3wsfztduvwpg)

[2.3 Funcionalidad de Particular	31](#_sqlxt3d1hpjw)

[Registro de Particular	31](#_s4ydsekk0epg)

[Listado de Catering	32](#_iu6ew55ify6c)

[Filtrado de catering	32](#_ppdiwaimmg1k)

[Buscar catering	33](#_b1q0y1pdyf0o)

[Detalles de catering	33](#_xx8z8t86yrt)

[Añadir review	34](#_wx39s2a21fuy)

[Reservar Catering(CORE)	35](#_d669rlnrezok)

[Mis reservas	40](#_2l2goaeqjhzo)

[Editar Reserva	41](#_nqcldst55vz2)

[Cancelar Reserva	41](#_gbv241pyzlsh)

[Chat con Empresa	42](#_82cci5ku78hj)

[2.4 Funcionalidad de Empleado	43](#_udu7vb5jhebm)

[Registro empleado	43](#_9shm2id1z6bj)

[Listado de ofertas	44](#_msvvme83v5jp)

[Aplicar a oferta	45](#_kry56e4emwc4)

[Listado de aplicaciones a ofertas enviadas	45](#_4k28u68adpnu)

[Perfil empleado	46](#_fnc6xijp67xp)

[Editar perfil empleado	46](#_knxjyqq09jtr)

[Cartas de recomendación	47](#_ms9w0mf5gxya)

[Chat con Empresa	47](#_h0qiiap4kqy5)

[Datos necesarios para realizar la revisión	49](#_jsm2q9qoex7w)

[Requisitos potenciales para usar el sistema	50](#_jhxs5pybp2vq)

[Link a la demo	50](#_6eq1dnqi35fc)

[Evaluación de Usabilidad	50](#_lhximwycsb56)

[Conclusiones	50](#_w48908okblry)
##






















### <a name="_dtyarly6zysm"></a><a name="_oz6624syu5h"></a>**1.Introducción**
En este documento se proporciona una visión general concisa de las funcionalidades del software, incluyendo su propósito, características principales y cómo funcionan. 

En este documento explicaremos las distintas funcionalidades implementadas hasta el momento en el software que estamos desarrollando, haciendo hincapié en cómo utilizar cada una de estas funcionalidades así como el propósito de estas y su rol en la aplicación.

También se hablará de cómo se ha revisado el software, cómo se ha probado cada funcionalidad, las pruebas de usabilidad y el  análisis del código.
### <a name="_l5rufmenkmpv"></a>**2. Funcionalidades** 
#### <a name="_9tzh197xg91q"></a>2.1 Funcionalidades Comunes
##### <a name="_ppjupmxb1smo"></a>**Login**
Url: /login


Página inicial para acceso a la página si ya se dispone de un usuario.

##### <a name="_w0hmy96ip0jq"></a>**Reseteo de contraseña**
Url: /reset\_password/

Página para que en caso de que un usuario no se acuerde de su contraseña tenga la posibilidad de recuperarla
##### <a name="_o0tko6m8t3ee"></a>**Elección de registro**
Url: /register\_choice


Página para elegir el tipo de usuario con el que se quiere acceder a la aplicación.
##### <a name="_ho9pg87nz5ot"></a>**Pasarela de pago**

Página común para el procesamiento de pagos. 

##### <a name="_yv8dtss3x9yq"></a>**About-us**
Url: /about-us


En esta página se muestran un poco de información relacionada con quienes somos, qué es banquetBuddy, cuales son nuestros servicios…

##### <a name="_wyu22ssat45b"></a>**Información de contacto**
Url: /contact

En esta página facilitamos nuestra información de contacto.

##### <a name="_xhrhf7rfjizs"></a>**Preguntas frecuentes**
Url: /faq

En esta página se muestran algunas preguntas frecuentes y respondemos a estas.

##### <a name="_lq2dsae3jwqb"></a>**Política de privacidad**
Url: /privacy-policy/

####
<a name="_nde74hf0e0ar"></a>En esta página mostramos nuestra política de privacidad y todas las cláusulas relacionadas con esta en detalle
##### <a name="_hh6bn2gg4qh3"></a>**Términos y condiciones**
Url: /terms-and-conditions



##### <a name="_lpfvrsweir3b"></a>**Reporte de errores**
Url: /error-report

#### <a name="_jagfzt1tk2pi"></a>
#### <a name="_3b62aqvwzr4o"></a>**2.2 Funcionalidad de Catering**
##### <a name="_77lcq0wkonlj"></a>**Registro Catering**
Url: /register\_company


Vista de registro de caterings, donde se puede registrar un catering seleccionando opciones como el tipo de plan que quieren contratar, la dirección de la compañía y el CIF (código de identificación fiscal).

Una vez hecho el registro,se deberá confirmar el correo electrónico que se ha ingresado durante el registro:

#####
##### <a name="_jgcgzuy4cxb8"></a><a name="_ca1ocx5uvfjn"></a>**Gestión de menús**
Primero tendremos que iniciar sesión como una empresa de catering con cualquier plan.Una vez iniciado sesión,nos aparecerá en la pantalla principal el botón de “Management”,el cual desplegará un submenú que incluye el botón de “My menús”:


Una vez accedido a la pestaña de menús,nos encontraremos con el listado de los menús que ofrece nuestra empresa,en el que podemos ver los nombres y descripciones de cada menú.Tendremos la posibilidad de editar([1](#hgk6f5aj6t61)) ,descartar el menú([2](#z464xlgxnpqb)) y añadir el menú([3](#npeclx6rflqe)):



1. <a name="hgk6f5aj6t61"></a>Si queremos editar el menú,nos aparecerá un formulario con los valores que se pueden editar:

1. <a name="z464xlgxnpqb"></a>Si presionamos el botón de descartar menú,nos aparecerá un mensaje de confirmación de que se ha eliminado el plato exitosamente:


1. <a name="npeclx6rflqe"></a>Si presionamos el botón de add menú,nos aparecerá un formulario para crear el menú








##### <a name="_n4699b99ajke"></a>**Perfil de catering**
Primero deberemos iniciar sesión con una empresa de catering cualquiera.Tras iniciar sesión,deberemos acceder al nombre de nuestra empresa en la cabecera de nuestra aplicación(en la parte superior derecha):



En caso de que queramos editar información de nuestro perfil,solo tenemos que seleccionar el botón “Edit Profile”
##### <a name="_c5vtmluj1vw9"></a>**Editar perfil de catering**
Url: /catering\_profile\_edit

Página donde se muestran los datos a editar de un perfil del tipo catering. 

##### <a name="_nw1bdciusw4y"></a>**Planes de subscripción**
Se puede acceder a través del botón “**Plan**” de la cabecera de la aplicación.Solo se puede ver si se ha iniciado sesión como empresa de catering o si no se ha iniciado sesión

Página donde muestran los planes de suscripción disponibles con las características de cada uno y un botón con la opción de cancelar la suscripción,que se encuentra según el plan de subscripción que tenga(si no está suscrito no le saldrá el botón) y, si la persona no está suscrita se muestran botones en todos los planes  que redirige a la pasarela de pago para cada plan.
##### <a name="_mcqrc236si8m"></a>**Gestión de Servicios**
Primero deberemos iniciar sesión como empresa de catering.Una vez hecho eso,podemos acceder a la pestaña de “Services” en la parte superior de la cabecera:

Una vez accedido a la pestaña de services,nos aparecerá todos nuestros servicios disponibles y la posibilidad de crear un servicio:

A continuación tendremos que rellenar el formulario que nos piden con datos correctos:

Si no hay errores durante el relleno del formulario,nos debería salir en el listado de caterings creados:

Podemos observar que tenemos tres opciones para tratar con los caterings:

1. **Employees**:muestra la lista de empleados actualmente trabajando en ese servicio de catering.Si presionamos ese botón,aparecería la siguiente vista:

1. **Edit:**Permite editar el servicio de catering.Al presionar el botón aparecería el formulario anterior en el que se puede modificar los valores actuales.

1. **Delete:**Permite borrar el servicio de catering.Al presionar aparecerá una pestaña de doble confirmación para evitar borrar un catering por accidente:


##### <a name="_1604n6misfbp"></a>Carta de recomendación a empleados 
Al acceder al listado de empleados anterior,habrá notado que existe un botón para añadir carta de recomendación.Al presionar el botón,aparecerá la siguiente pantalla:

Tras guardar la carta de recomendación en el sistema,se mostrará que se ha enviado correctamente.

Listado de platos de un catering, donde se muestra el nombre del plato, el menú al que pertenece, una descripción, y el precio. Además ofrece las opciones de edición y eliminación de platos de un menú

##### <a name="_wbkt9afcptdz"></a>**Gestión de platos**
Primero hay que iniciar sesión con una compañía de catering con cualquier tipo de plan.Una vez iniciado sesión,tendremos que seleccionar el botón de “Management” en la cabecera de la página,que desplegará un submenú donde se podrá ver el botón de “My plates”:



A continuación se nos mostrará un listado de todos los platos que tenemos disponibles,teniendo la posibilidad de filtrar por menú para facilitar su navegabilidad:


Esta vista nos dará la posibilidad de añadir platos a un menú(1),editar un plato(2) y borrar un plato de un menú(3)

1. Para crear un plato,tendremos que presionar el botón de “Add plates”:




1. Para editar un menú,tendremos que presionar el botón de editar en el menú deseado:


1. Para eliminar un menú,tendremos que presionar el botón de eliminar en el menú deseado:






##### <a name="_wda1vzgh4js9"></a>**Gestión de ofertas**
Necesitaremos iniciar sesión como una compañía de catering con Plan PREMIUM PRO.Una vez iniciado sesión, tendremos que presionar el botón de “Offers” en la cabecera de la página:



En esta vista tendremos acceso al listado de ofertas,cada una con tres interacciones disponibles: 

1. **Applications:**permite consultar los aplicantes a dicha oferta de empleo

1. **Edit:**Permite editar la oferta en cuestión:


1. **Delete:**Permite eliminar la oferta en cuestión:


##### <a name="_okrob04e0q4v"></a>**Contratación de empleo(CORE)**
Se trata de una interacción MATCHMAKING,donde interviene por una parte el empleado y por otra la empresa de catering.Esta interacción procede de la siguiente manera:

1. Creación de oferta de empleo:La empresa con PLAN PREMIUM\_PRO primero debe publicar la oferta de empleo a través de la sección “Offers”:

   1. Al acceder a “Offers”,saldrá un listado de las ofertas que la empresa ha publicado,dando la posibilidad de crear nuevas ofertas a través del botón offers:

   1. Tras rellenar el formulario de oferta,se verá la oferta que hemos publicado y el empleado podrá ver la oferta que hemos publicado:



   1. una vez aplicada,el empresario deberá aceptarla desde la vista de offers:





A continuación ya es decisión de la empresa contratar o no contratar al aspirante al puesto.

Permite crear una nueva oferta de empleo rellenando el formulario a través del listado de empleos en la pestaña “Offers”



##### <a name="_brd9129g2jrq"></a>**Reservas**
Una vez iniciado sesión como empresa de catering,se tendrá que acceder al botón de “Management” en la cabecera de la página,que contiene el botón de “My bookings”:


Aquí se tendrá que seleccionar el servicio de catering que quieras consultar:


Aquí se podrá ver el listado de reservas que tiene el servicio de catering elegido,pudiendo acceder a los detalles de cada reserva mediante el botón de “View details”:



##### <a name="_8equoco94nuq"></a>**Calendario**
Primero deberemos iniciar sesión como una empresa de catering con plan PREMIUM o superior.Una vez iniciado sesión,tenemos que presionar el botón de “Calendar” en la cabecera de la página:

Tenemos que seleccionar el servicio de catering que se quiera consultar:

A continuación se mostrará un calendario con los días que la empresa tiene eventos que atender,junto a otra información de interés como pueden ser el número de eventos que hay ese mes o la fecha del próximo evento.

Si presionamos en cualquier día señalado,podremos ver los eventos que hay ese día:


##### <a name="_3wsfztduvwpg"></a>**Gestión de tareas(PREMIUM)**
Primero deberemos iniciar sesión como una empresa de catering que tenga el plan PREMIUM(la restricción de acceso no está todavía por un error de revisión),de otra forma se le denegará el acceso a dicha funcionalidad(si no hay ninguna empresa con ese plan de precios,puede usted aplicar a un plan superior con la información de tarjeta incluida en el apartado”requisitos potenciales para usar el sistema”).

Una vez iniciado sesión como empresa con plan PREMIUM o superior,acceda al botón de management,en el que aparecerá un submenú que contiene el botón “My bookings”:


Una vez accedido al apartado de “my bookings,tendremos que acceder a una reserva que esté **CONFIRMADA**:

Una vez accedido a la reserva,se desplegará un tablero kanban donde se mostrarán las tareas y sus estados:

Para crear una tarea,tenemos que presionar el botón de “Add Task” y aparecerá un formulario a rellenar.Una vez rellenado el formulario,aparecerá la tarea en “Pending” por defecto:


Una vez creada,se puede desplazar tareas fácilmente con el ratón al estado deseado(como si se tratase de una issue de un project de github)
#### <a name="_sqlxt3d1hpjw"></a>**2.3 Funcionalidad de Particular**

##### <a name="_s4ydsekk0epg"></a>**Registro de Particular**
Url: /caterings/register\_particular

Una vez hecho el registro,se deberá confirmar el correo electrónico que se ha ingresado durante el registro:



##### <a name="_d669rlnrezok"></a>**Reservar Catering(CORE)**
url: /particular/(id)/book

Se trata de una interacción MATCHMAKING,donde interviene por una parte el particular que quiere contratar el empleo y la empresa de catering.Esta interacción procede de la siguiente manera:

1. El particular inicia sesión con su cuenta y se dirige a la pestaña “Caterings en la cabecera de la página:

A continuación se mostrará el listado de caterings disponibles para el particular,mostrando descripción y la posibilidad de ver detalles de la aplicación.Para contratar el catering o dejar una reseña,se deberá pulsar el botón “View Details”:



1. Después de pulsar el botón de reservar(“Book”),te pedirá que elijas el menú que se va a contratar para el evento,seguido del pago del servicio(son datos ficticios los mostrados aquí):


1. Una vez contratado el servicio,se recibirá un mensaje de confirmación de que el servicio se ha contratado de forma exitosa:

1. El particular podrá ver el servicio que se ha contratado en la sección “My bookings” en la cabecera de la página

1. Iniciando sesión como la empresa que posee el servicio,en la pestaña de notificaciones se podrá ver que el particular ha contratado un servicio de catering de la propia empresa.También se podrá consultar dicha reserva en el botón de “management”











##### <a name="_2l2goaeqjhzo"></a>**Mis reservas**
Primero deberemos iniciar sesión como particular.Una vez iniciado sesión como particular,tendremos que presionar el botón de “My bookings” en la cabecera de la página:



Una vez presionado,accederemos al listado de nuestras reservas de servicios de catering:


Muestra las reservas de caterings que ha realizado una persona, dando la posibilidad de editar y cancelar la reserva.En caso de que queramos cancelar la reserva,se nos mostrará una pantalla de confirmación con el fin de evitar borrados accidentales:

##### <a name="_82cci5ku78hj"></a>**Chat con Empresa**
Una vez iniciado sesión como cualquier particular,en la cabecera de la página se podrá ver un apartado con el nombre de “Chats”:

Una vez presionado,se accederá a un listado de servicios de caterings disponibles con los que se podrá entablar una conversación.Si queremos iniciar una conversación con algún servicio,solo tenemos que presionar el botón de “Chat”:

A continuación se desplegará una pantalla de chat donde se podrá preguntar al encargado del servicio de catering:

#### <a name="_udu7vb5jhebm"></a>**2.4 Funcionalidad de Empleado**
##### <a name="_9shm2id1z6bj"></a>**Registro empleado**
Url: /register\_employee


Permite que un empleado se registre, introduciendo los datos correspondientes. 

Una vez hecho el registro,se deberá confirmar el correo electrónico que se ha ingresado durante el registro:


##### <a name="_msvvme83v5jp"></a>**Gestión de ofertas para empleado**
Primero deberemos iniciar sesión como empleado.Una vez iniciado sesión,podemos acceder al listado de ofertas disponibles en la aplicación:


En caso de que queramos aplicar a alguna oferta,tenemos que presionar el botón “Apply” de aquella oferta que queramos aplicar.Una vez presionado el botón,se enviará una solicitud de aplicación a ese puesto,y saldrá la siguiente pantalla de confirmación:


Por otro lado,si queremos ver las ofertas a las que ya hemos aplicado,tenemos que presionar el botón de “Offers applied” en la cabecera de la aplicación:


##### <a name="_fnc6xijp67xp"></a>**Perfil empleado**
Primero tendremos que iniciar sesión como empleado.Una vez iniciado sesión,tendremos que presionar el botón con nuestro nombre de usuario en la cabecera de la página(esquina superior derecha):


En caso de que queramos editar nuestro perfil de usuario,podemos darle al botón de “Edit profile”.También se puede acceder a tus cartas de recomendación mediante el botón “Recommendation Letters”,que llevará a la siguiente vista:



Muestra el perfil con los datos del empleado, con las opciones de editar el perfil y ver las cartas de recomendación recibidas.



##### <a name="_h0qiiap4kqy5"></a>**Chat con Empresa**
**Este caso de uso se ejerce de la misma manera que con el particular,pero necesitaremos iniciar sesión como empleado**. Una vez iniciado sesión como cualquier empleado,en la cabecera de la página se podrá ver un apartado con el nombre de “Chats”:

Una vez presionado,se accederá a un listado de servicios de caterings disponibles con los que se podrá entablar una conversación:

A continuación se desplegará una pantalla de chat donde se podrá preguntar al encargado del servicio de catering:



### <a name="_jsm2q9qoex7w"></a>**Datos necesarios para realizar la revisión**
- URL de la landing page: [landing page](https://ispp-grupo-8.github.io/banquetbuddy.landing-page/)

`	`Dato para campo pdf: [curriculum.pdf](https://drive.google.com/file/d/1SptPLPMQQJKqRHs6P4Lqz25XMgDvUK4w/view?usp=sharing)

- URL plataforma desplegada: [Link] (http://banquetbuddys3.pythonanywhere.com/)
- URL repositorio Github: [Link](https://github.com/ISPP-GRUPO-8/BANQUETBUDDY)


- URL y credenciales de la herramienta de seguimiento: [Link](ttp://dashboard.bluejay.governify.io/dashboard/script/dashboardLoader.js?dashboardURL=https://reporter.bluejay.governify.io/api/v4/dashboards/tpa-ISPP-2024-GH-ISPP-GRUPO-8_BANQUETBUDDY/main)
- Credenciales: user: user 

` `password: bluejay

- URL de la herramienta de seguimiento de tiempo:
  - URL: [Link](https://app.clockify.me/projects/65ba7f5a293b89339166ab29/edit)



### <a name="_jhxs5pybp2vq"></a>**Requisitos potenciales para usar el sistema**
En caso de que necesite hacer cualquier pago dentro del sistema,una tarjeta de crédito que usted pueda usar es:4242 4242 4242 4242,y en lo demás puede poner cualquier cosa(tenga en cuenta que tiene que poner fecha de caducidad posterior al día actual)
### <a name="_6eq1dnqi35fc"></a>**Link a la demo**
[Demo-semana-10_1.mp4](https://drive.google.com/file/d/1rgcQ_5rRxUsTmqwZ2Xq2pM5FDSdA3xDv/view?usp=sharing)
### <a name="_lhximwycsb56"></a>**Evaluación de Usabilidad**
Bajo nuestro punto de vista la aplicación se puede usar de forma fácil e intuitiva. Aun así, hay aspectos que no no están todo lo bien que nos gustaría, pero somos conscientes y tenemos previsto mejorar todo lo posible la web en el tercer sprint.

Otro punto a tener en cuenta es el feedback recibido por parte de los usuarios pilotos, que no está llegando en estos momentos. Estos datos los usaremos para tener puntos de vista objetivos por parte de personas ajenas al desarrollo de la aplicación y añadir mejoras propuestas en este tercer sprint. 
### <a name="_w48908okblry"></a>**Conclusiones**
En conclusión la mayoría de requisitos se han cumplido y las funcionalidades implementadas funcionan correctamente. Podemos remarcar las diferencias de estilos en diversas páginas como un punto a mejorar en el último sprint, así como algunos pequeños errores y bad smells que se han encontrado durante la revisión del código, como urls repetidas y algunos vínculos que no aparecen en la barra de navegación cuando se cambia de vista, por lo demás todo lo que se ha probado ha funcionado correctamente en la revisión. 

