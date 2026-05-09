from django.contrib import admin
from .models import Doctor, Nurse, Specialty, Schedule, Leave

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialty', 'consultation_fee', 'is_active']
    list_filter  = ['specialty', 'is_active']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'get_day_of_week_display', 'start_time', 'end_time']
    list_filter  = ['doctor', 'day_of_week']