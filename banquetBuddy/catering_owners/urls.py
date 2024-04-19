from django.urls import path
from . import views
from core.views import home
from django.urls import path
from .views import *

urlpatterns = [
    path("applicants/<int:offer_id>/", employee_applications, name="applicants"),
    path(
        "view-reservations/<int:catering_service_id>/",
        view_reservations,
        name="view_reservations",
    ),
    path(
        "view-reservations/<int:catering_service_id>/view_reservation/<int:event_id>/",
        view_reservation,
        name="view_reservation",
    ),
    path(
        "catering-calendar/",
        catering_calendar_preview,
        name="catering_calendar_preview",
    ),
    path(
        "catering-calendar/<int:catering_service_id>/<int:year>/<int:month>",
        catering_calendar_view,
        name="catering_calendar",
    ),
    path(
        "catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/next_month/",
        next_month_view,
        name="next_month",
    ),
    path(
        "catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/prev_month/",
        prev_month_view,
        name="prev_month",
    ),
    path(
        "catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/<int:day>/",
        reservations_for_day,
        name="reservations_for_day",
    ),
    path("", home, name="home"),
    path("register_company", views.register_company, name="register_company"),
    path('catering_books', catering_books, name='catering_books'),
    path('catering_books/<int:event_id>/edit', book_catering_edit, name='catering_books_edit'),
    path('catering_books/<int:event_id>/cancel', book_catering_cancel, name='catering_books_cancel'),
    path('list_menus/', views.list_menus, name='list_menus'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('edit_menu/<int:menu_id>/', views.edit_menu, name='edit_menu'),
    path('delete_menu/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path('catering_profile_edit', views.catering_profile_edit, name='catering_profile_edit'),
    path('create_offer', create_offer, name='create_offer'),
    path('offer_list', offer_list, name='offer_list'),
    path('employee_record/<int:employee_id>/', employee_record_list, name='employee_record'),
    path('hire_employee/<int:employee_id>/', hire_employee, name='hire_employee'),
    path('delete_offer/<int:offer_id>/', delete_offer, name='delete_offer'),
    path('edit_offer/<int:offer_id>/', edit_offer, name='edit_offer'),
    path('confirm_delete_offer/<int:offer_id>/', confirm_delete_offer, name='confirm_delete_offer'),
    path('my_bookings/',my_bookings_preview, name='my_bookings'),
    path('service/<int:service_id>/employees', list_employee, name='list_employee'),
    path('service/<int:service_id>/employees/<int:employee_id>/recommendation_letter', create_recommendation_letter, name='recommendation_letter'),
    path("services/", get_catering_services, name="services"),
    path("create_service/", create_catering_service, name="create_service"),
    path("update_service/<int:service_id>/", update_catering_service, name="update_service"),
    path('delete_service/<int:service_id>/', delete_service, name='delete_service'),
    path('confirm_delete_service/<int:service_id>/', confirm_delete_service, name='confirm_delete_service'),
    path('plates/', views.list_plates, name='list_plates'),
    path('plates/add/', views.add_plate, name='add_plate'),
    path('plates/<int:plate_id>/edit/', views.edit_plate, name='edit_plate'),
    path('plates/<int:plate_id>/delete/', views.delete_plate, name='delete_plate'),
    path('chats/', listar_caterings_particular, name='listar_caterings_particular'),
    path('service/<int:service_id>/employees', list_employee, name='list_employee'),
    path('employees/edit/<int:employee_work_service_id>/', edit_employee_termination, name='edit_employee_termination'),


    # CAMBIO DE PLAN
    path("catering_unsuscribe/", catering_unsuscribe, name="catering_unsuscribe"),

    path('process_base/', payment_process_base, name='process_base'),
    path('completed_base/', payment_completed_base, name='completed_base'),

    path('process_premium/', payment_process_premium, name='process_premium'),
    path('completed_premium/', payment_completed_premium, name='completed_premium'),

    path('process_pro/', payment_process_pro, name='process_pro'),
    path('completed_pro/', payment_completed_pro, name='completed_pro'),

    path('canceled/', payment_canceled, name='canceled'),
    path('chat/<int:id>/', chat_view, name='chat'),



]

# Configuración para servir archivos estáticos y de medios durante el desarrollo
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
