from django import forms
from .models import Consultation, Prescription, PrescriptionItem, LabRequest


class ConsultationForm(forms.ModelForm):
    class Meta:
        model  = Consultation
        fields = ['patient', 'doctor', 'appointment', 'motif',
                  'clinical_exam', 'diagnosis', 'treatment', 'notes', 'follow_up_date']
        widgets = {
            'patient':       forms.Select(attrs={'class': 'form-select'}),
            'doctor':        forms.Select(attrs={'class': 'form-select'}),
            'appointment':   forms.Select(attrs={'class': 'form-select'}),
            'motif':         forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'clinical_exam': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes':         forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'follow_up_date':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model  = PrescriptionItem
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage':          forms.TextInput(attrs={'class': 'form-control'}),
            'frequency':       forms.TextInput(attrs={'class': 'form-control'}),
            'duration':        forms.TextInput(attrs={'class': 'form-control'}),
            'instructions':    forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class LabRequestForm(forms.ModelForm):
    class Meta:
        model  = LabRequest
        fields = ['type', 'description']
        widgets = {
            'type':        forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }