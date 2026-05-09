from django import forms
from .models import Doctor, Nurse, Specialty, Schedule, Leave


class DoctorForm(forms.ModelForm):
    class Meta:
        model  = Doctor
        fields = ['user', 'specialty', 'rpps_number', 'consultation_fee', 'office_number', 'bio']
        widgets = {
            'user':             forms.Select(attrs={'class': 'form-select'}),
            'specialty':        forms.Select(attrs={'class': 'form-select'}),
            'rpps_number':      forms.TextInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'office_number':    forms.TextInput(attrs={'class': 'form-control'}),
            'bio':              forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model  = Schedule
        fields = ['day_of_week', 'start_time', 'end_time', 'slot_duration']
        widgets = {
            'day_of_week':    forms.Select(attrs={'class': 'form-select'}),
            'start_time':     forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time':       forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'slot_duration':  forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model  = Leave
        fields = ['doctor', 'start_date', 'end_date', 'reason']
        widgets = {
            'doctor':     forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }