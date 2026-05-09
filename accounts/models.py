from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN',       'Administrateur'),
        ('DOCTOR',      'Médecin'),
        ('SECRETARY',   'Secrétaire'),
        ('NURSE',       'Infirmier/Infirmière'),
        ('PATIENT',     'Patient'),
    ]

    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SECRETARY', verbose_name="Rôle")
    phone       = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    photo       = models.ImageField(upload_to='users/photos/', blank=True, null=True, verbose_name="Photo")
    is_verified = models.BooleanField(default=False, verbose_name="Email vérifié")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    # Propriétés utiles
    @property
    def is_admin(self):    return self.role == 'ADMIN'
    @property
    def is_doctor(self):   return self.role == 'DOCTOR'
    @property
    def is_secretary(self):return self.role == 'SECRETARY'
    @property
    def is_nurse(self):    return self.role == 'NURSE'
    @property
    def full_name(self):   return f"{self.first_name} {self.last_name}".strip() or self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"