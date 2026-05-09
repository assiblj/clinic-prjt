from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name  = forms.CharField(max_length=50, label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email      = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role       = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label='Rôle',
        widget=forms.Select(attrs={'class': 'form-select'}))
    phone      = forms.CharField(max_length=20, required=False, label='Téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model  = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'photo', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control'}),
            'photo':      forms.FileInput(attrs={'class': 'form-control'}),
            'role':       forms.Select(attrs={'class': 'form-select'}),
        }