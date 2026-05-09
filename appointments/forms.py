from django import forms
from .models import Appointment
from staff.models import Doctor
from patients.models import Patient


class AppointmentForm(forms.ModelForm):
    class Meta:
        model  = Appointment
        fields = ['patient', 'doctor', 'date_time', 'duration', 'motif', 'type', 'status', 'notes']
        widgets = {
            'patient':   forms.Select(attrs={'class': 'form-select'}),
            'doctor':    forms.Select(attrs={'class': 'form-select'}),
            'date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration':  forms.NumberInput(attrs={'class': 'form-control'}),
            'motif':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'type':      forms.Select(attrs={'class': 'form-select'}),
            'status':    forms.Select(attrs={'class': 'form-select'}),
            'notes':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }