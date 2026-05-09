from django.contrib import admin
from .models import Appointment, TimeSlot

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ['patient', 'doctor', 'date_time', 'type', 'status']
    list_filter   = ['status', 'type', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name']
    ordering      = ['-date_time']