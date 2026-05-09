from django.contrib import admin

# Register your models here.
from .models import Patient, MedicalRecord, VitalSigns


class MedicalRecordInline(admin.StackedInline):
    model  = MedicalRecord
    extra  = 0

class VitalSignsInline(admin.TabularInline):
    model  = VitalSigns
    extra  = 0
    readonly_fields = ['measured_at']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display   = ['file_number', 'full_name', 'age', 'gender', 'phone', 'city', 'is_active']
    list_filter    = ['gender', 'blood_group', 'city', 'is_active']
    search_fields  = ['first_name', 'last_name', 'cin', 'file_number', 'phone']
    readonly_fields= ['file_number', 'created_at', 'updated_at']
    inlines        = [MedicalRecordInline, VitalSignsInline]

    def full_name(self, obj): return obj.full_name
    full_name.short_description = 'Nom complet'

    def age(self, obj): return f"{obj.age} ans"
    age.short_description = 'Âge'