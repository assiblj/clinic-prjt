from django.contrib import admin
from .models import Consultation, Prescription, PrescriptionItem, LabRequest

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display  = ['patient', 'doctor', 'date', 'diagnosis']
    search_fields = ['patient__first_name', 'patient__last_name']
    ordering      = ['-date']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'created_at']
    inlines      = [PrescriptionItemInline]