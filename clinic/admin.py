from django.contrib import admin
from .models import Appointment, Review, ContactMessage


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient_name', 'doctor', 'appointment_date', 'appointment_time', 'status', 'booking_type')
    list_filter = ('status', 'booking_type', 'appointment_date')
    search_fields = ('appointment_id', 'patient_name', 'phone', 'doctor')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'rating', 'department', 'approved')
    list_filter = ('approved', 'rating')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'submitted_at')
    search_fields = ('name', 'phone', 'email')
