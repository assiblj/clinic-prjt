from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Consultation, Prescription, PrescriptionItem, LabRequest
from .forms import ConsultationForm, PrescriptionItemForm, LabRequestForm


@login_required
def consultation_list(request):
    consultations = Consultation.objects.filter(
        is_active=True
    ).select_related('patient', 'doctor__user').order_by('-date')
    return render(request, 'consultations/consultation_list.html',
                  {'consultations': consultations})


@login_required
def consultation_create(request):
    ItemFormSet = inlineformset_factory(
        Prescription, PrescriptionItem,
        form=PrescriptionItemForm, extra=3, can_delete=True
    )
    form = ConsultationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        consultation = form.save(commit=False)
        consultation.created_by = request.user
        consultation.save()
        # Marquer le RDV comme honoré
        if consultation.appointment:
            consultation.appointment.complete()
        messages.success(request, 'Consultation enregistrée.')
        return redirect('consultations:detail', pk=consultation.pk)
    return render(request, 'consultations/consultation_form.html', {
        'form': form, 'title': 'Nouvelle consultation'
    })


@login_required
def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    prescription = getattr(consultation, 'prescription', None)
    lab_requests = consultation.lab_requests.all()
    return render(request, 'consultations/consultation_detail.html', {
        'consultation': consultation,
        'prescription': prescription,
        'lab_requests': lab_requests,
    })


@login_required
def prescription_add(request, consultation_pk):
    consultation = get_object_or_404(Consultation, pk=consultation_pk)
    ItemFormSet  = inlineformset_factory(
        Prescription, PrescriptionItem,
        form=PrescriptionItemForm, extra=3, can_delete=False
    )
    if request.method == 'POST':
        prescription, _ = Prescription.objects.get_or_create(
            consultation=consultation,
            defaults={
                'patient': consultation.patient,
                'doctor':  consultation.doctor,
                'created_by': request.user,
            }
        )
        formset = ItemFormSet(request.POST, instance=prescription)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Ordonnance enregistrée.')
            return redirect('consultations:detail', pk=consultation_pk)
    else:
        prescription, _ = Prescription.objects.get_or_create(
            consultation=consultation,
            defaults={
                'patient': consultation.patient,
                'doctor':  consultation.doctor,
                'created_by': request.user,
            }
        )
        formset = ItemFormSet(instance=prescription)
    return render(request, 'consultations/prescription_form.html', {
        'formset': formset, 'consultation': consultation
    })


@login_required
def labrequest_add(request, consultation_pk):
    consultation = get_object_or_404(Consultation, pk=consultation_pk)
    form = LabRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        lab = form.save(commit=False)
        lab.consultation = consultation
        lab.patient      = consultation.patient
        lab.created_by   = request.user
        lab.save()
        messages.success(request, 'Demande d\'examen ajoutée.')
        return redirect('consultations:detail', pk=consultation_pk)
    return render(request, 'consultations/labrequest_form.html', {
        'form': form, 'consultation': consultation
    })