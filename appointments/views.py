from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_list(request):
    today = timezone.now().date()
    upcoming = Appointment.objects.filter(
        date_time__date__gte=today, is_active=True
    ).select_related('patient', 'doctor__user').order_by('date_time')
    past = Appointment.objects.filter(
        date_time__date__lt=today, is_active=True
    ).select_related('patient', 'doctor__user').order_by('-date_time')[:10]
    return render(request, 'appointments/appointment_list.html', {
        'upcoming': upcoming, 'past': past, 'today': today
    })


@login_required
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appt = form.save(commit=False)
        appt.created_by = request.user
        appt.save()
        messages.success(request, f'RDV créé pour {appt.patient.full_name}.')
        return redirect('appointments:list')
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 'title': 'Nouveau rendez-vous'
    })


@login_required
def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appt)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'RDV modifié.')
        return redirect('appointments:list')
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 'title': 'Modifier le rendez-vous'
    })


@login_required
def appointment_cancel(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.cancel()
    messages.warning(request, f'RDV annulé.')
    return redirect('appointments:list')


@login_required
def appointment_confirm(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.confirm()
    messages.success(request, 'RDV confirmé.')
    return redirect('appointments:list')