# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Patient, MedicalRecord, VitalSigns
from .forms import PatientForm, MedicalRecordForm, VitalSignsForm


@login_required
def patient_list(request):
    q = request.GET.get('q', '')
    patients = Patient.objects.filter(is_active=True)
    if q:
        patients = patients.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(cin__icontains=q) | Q(file_number__icontains=q) |
            Q(phone__icontains=q)
        )
    paginator = Paginator(patients, 15)
    page      = paginator.get_page(request.GET.get('page'))
    return render(request, 'patients/patient_list.html', {'page_obj': page, 'query': q})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_active=True)
    record, _  = MedicalRecord.objects.get_or_create(patient=patient)
    vitals     = patient.vital_signs.all()[:5]
    return render(request, 'patients/patient_detail.html', {
        'patient': patient, 'record': record, 'vitals': vitals
    })


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        patient = form.save(commit=False)
        patient.created_by = request.user
        patient.save()
        MedicalRecord.objects.create(patient=patient, created_by=request.user)
        messages.success(request, f'Patient {patient.full_name} enregistré (N° {patient.file_number}).')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Nouveau patient'})


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form    = PatientForm(request.POST or None, request.FILES or None, instance=patient)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Dossier patient mis à jour.')
        return redirect('patients:detail', pk=pk)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Modifier le patient'})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.soft_delete()
        messages.success(request, f'Patient {patient.full_name} archivé.')
        return redirect('patients:list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


@login_required
def medical_record_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    record, _ = MedicalRecord.objects.get_or_create(patient=patient)
    form = MedicalRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Dossier médical mis à jour.')
        return redirect('patients:detail', pk=pk)
    return render(request, 'patients/medical_record_form.html', {'form': form, 'patient': patient})


@login_required
def vital_signs_add(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form    = VitalSignsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        v = form.save(commit=False)
        v.patient = patient
        v.save()
        messages.success(request, 'Constantes enregistrées.')
        return redirect('patients:detail', pk=pk)
    return render(request, 'patients/vital_signs_form.html', {'form': form, 'patient': patient})