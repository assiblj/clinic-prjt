from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Doctor, Specialty, Schedule
from .forms import DoctorForm, ScheduleForm, LeaveForm


@login_required
def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True).select_related('user', 'specialty')
    return render(request, 'staff/doctor_list.html', {'doctors': doctors})


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    schedules = doctor.schedules.all()
    leaves = doctor.leaves.all().order_by('-start_date')[:5]
    return render(request, 'staff/doctor_detail.html', {
        'doctor': doctor, 'schedules': schedules, 'leaves': leaves
    })


@login_required
def doctor_create(request):
    form = DoctorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        doctor = form.save(commit=False)
        doctor.created_by = request.user
        doctor.save()
        messages.success(request, f'Médecin {doctor.full_name} ajouté.')
        return redirect('staff:doctor_list')
    return render(request, 'staff/doctor_form.html', {'form': form, 'title': 'Nouveau médecin'})


@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form   = DoctorForm(request.POST or None, instance=doctor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Médecin modifié.')
        return redirect('staff:doctor_detail', pk=pk)
    return render(request, 'staff/doctor_form.html', {'form': form, 'title': 'Modifier médecin'})


@login_required
def schedule_add(request, doctor_pk):
    doctor = get_object_or_404(Doctor, pk=doctor_pk)
    form   = ScheduleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        s = form.save(commit=False)
        s.doctor = doctor
        s.save()
        messages.success(request, 'Planning ajouté.')
        return redirect('staff:doctor_detail', pk=doctor_pk)
    return render(request, 'staff/schedule_form.html', {'form': form, 'doctor': doctor})