# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .models import CustomUser
from .forms import LoginForm, RegisterUserForm, UpdateUserForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Bienvenue, {user.full_name} !')
        return redirect(request.GET.get('next', 'core:dashboard'))
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('accounts:profile')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


def is_admin(user):
    return user.is_authenticated and user.is_admin


@user_passes_test(is_admin, login_url='/accounts/login/')
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@user_passes_test(is_admin, login_url='/accounts/login/')
def user_create(request):
    form = RegisterUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f'Utilisateur {user.full_name} créé avec succès.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Créer un utilisateur'})


@user_passes_test(is_admin, login_url='/accounts/login/')
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = UpdateUserForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Utilisateur modifié avec succès.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Modifier l\'utilisateur'})


@user_passes_test(is_admin, login_url='/accounts/login/')
def user_toggle_active(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    status = 'activé' if user.is_active else 'désactivé'
    messages.success(request, f'Utilisateur {user.full_name} {status}.')
    return redirect('accounts:user_list')