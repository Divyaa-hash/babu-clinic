"""
URL configuration for babuclinic project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from clinic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('doctors/', views.doctors, name='doctors'),
    path('appointment/', views.appointment, name='appointment'),
    path('contact/', views.contact, name='contact'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),
    path('admin-appointments/', views.admin_appointments, name='admin_appointments'),
    path('walkin-appointment/', views.walkin_appointment, name='walkin_appointment'),
    path('track-appointment/', views.track_appointment, name='track_appointment'),
    path('api/appointment/', views.api_appointment, name='api_appointment'),
    path('api/contact/', views.api_contact, name='api_contact'),
    path('api/walkin-appointment/', views.api_walkin_appointment, name='api_walkin_appointment'),
    path('api/track-appointment/', views.api_track_appointment, name='api_track_appointment'),
    path('api/get-appointments/', views.api_get_appointments, name='api_get_appointments'),
    path('api/appointment-statistics/', views.api_appointment_statistics, name='api_appointment_statistics'),
    path('api/update-appointment-status/', views.api_update_appointment_status, name='api_update_appointment_status'),
    path('api/submit-review/', views.api_submit_review, name='api_submit_review'),
    path('api/get-reviews/', views.api_get_reviews, name='api_get_reviews'),
    path('api/delete-appointment/', views.api_delete_appointment, name='api_delete_appointment'),
    path('api/get-doctor-department/', views.api_get_doctor_department, name='api_get_doctor_department'),
    path('api/export-appointments-pdf/', views.api_export_appointments_pdf, name='api_export_appointments_pdf'),
    path('api/export-single-appointment-pdf/', views.api_export_single_appointment_pdf, name='api_export_single_appointment_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
