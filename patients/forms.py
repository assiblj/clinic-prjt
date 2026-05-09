from django import forms
from .models import Patient, MedicalRecord, VitalSigns


class PatientForm(forms.ModelForm):
    class Meta:
        model  = Patient
        fields = [
            'first_name','last_name','date_of_birth','gender','cin',
            'blood_group','marital_status','photo','phone','phone_alt',
            'email','address','city','insurance_name','insurance_number',
        ]
        widgets = {
            'first_name':    forms.TextInput(attrs={'class':'form-control'}),
            'last_name':     forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'gender':        forms.Select(attrs={'class':'form-select'}),
            'cin':           forms.TextInput(attrs={'class':'form-control'}),
            'blood_group':   forms.Select(attrs={'class':'form-select'}),
            'marital_status':forms.Select(attrs={'class':'form-select'}),
            'photo':         forms.FileInput(attrs={'class':'form-control'}),
            'phone':         forms.TextInput(attrs={'class':'form-control'}),
            'phone_alt':     forms.TextInput(attrs={'class':'form-control'}),
            'email':         forms.EmailInput(attrs={'class':'form-control'}),
            'address':       forms.Textarea(attrs={'class':'form-control','rows':2}),
            'city':          forms.TextInput(attrs={'class':'form-control'}),
            'insurance_name':forms.TextInput(attrs={'class':'form-control'}),
            'insurance_number':forms.TextInput(attrs={'class':'form-control'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model  = MedicalRecord
        fields = ['allergies','chronic_diseases','past_surgeries','family_history',
                  'current_medications','notes']
        widgets = {f: forms.Textarea(attrs={'class':'form-control','rows':3})
                   for f in ['allergies','chronic_diseases','past_surgeries',
                              'family_history','current_medications','notes']}


class VitalSignsForm(forms.ModelForm):
    class Meta:
        model  = VitalSigns
        fields = ['weight','height','blood_pressure_sys','blood_pressure_dia',
                  'temperature','heart_rate']
        widgets = {f: forms.NumberInput(attrs={'class':'form-control'})
                   for f in ['weight','height','blood_pressure_sys',
                              'blood_pressure_dia','temperature','heart_rate']}