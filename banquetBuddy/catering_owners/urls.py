from django.urls import path
from . import views
from core.views import home
from django.conf import settings

urlpatterns = [
    path('applicants/<int:offer_id>/', views.employee_applications, name='applicants'),
    path('view-reservations/<int:catering_service_id>/', views.view_reservations, name='view_reservations'),
    path('view-reservations/<int:catering_service_id>/view_reservation/<int:event_id>/', views.view_reservation, name='view_reservation'),
    path('catering-calendar/', views.catering_calendar_preview, name='catering_calendar_preview'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/', views.catering_calendar_view, name='catering_calendar'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/next_month/', views.next_month_view, name='next_month'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/prev_month/', views.prev_month_view, name='prev_month'),
    path('catering-calendar/<int:catering_service_id>/<int:year>/<int:month>/<int:day>/', views.reservations_for_day, name='reservations_for_day'),
    path('', home, name='home'),
    path('register_company', views.register_company, name='register_company'),
    path('catering_profile_edit', views.catering_profile_edit, name='catering_profile_edit'),
    path('catering_books', views.catering_books, name='catering_books'),
    path('catering_books/<int:event_id>/edit', views.book_catering_edit, name='catering_books_edit'),
    path('catering_books/<int:event_id>/cancel', views.book_catering_cancel, name='catering_books_cancel'),
    path('list_menus/', views.list_menus, name='list_menus'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('edit_menu/<int:menu_id>/', views.edit_menu, name='edit_menu'),
    path('delete_menu/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path('create_offer', views.create_offer, name='create_offer'),
    path('offer_list', views.offer_list, name='offer_list'),
    path('apply_offer/<int:offer_id>/', views.apply_offer, name='apply_offer'),
    path('delete_offer/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('edit_offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('confirm_delete_offer/<int:offer_id>/', views.confirm_delete_offer, name='confirm_delete_offer'),
    path('my_bookings/', views.my_bookings_preview, name='my_bookings'),
    path('catering_unsuscribe/', views.catering_unsuscribe, name='catering_unsuscribe'),
]

# Configuración para servir archivos estáticos y de medios durante el desarrollo
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
