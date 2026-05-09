from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from core.models import BaseModel


class Patient(BaseModel):
    BLOOD_GROUP_CHOICES = [
        ('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),
        ('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-'),
    ]
    GENDER_CHOICES  = [('M','Masculin'),('F','Féminin'),('OTHER','Autre')]
    MARITAL_CHOICES = [
        ('SINGLE','Célibataire'),('MARRIED','Marié(e)'),
        ('DIVORCED','Divorcé(e)'),('WIDOWED','Veuf/Veuve'),
    ]

    first_name       = models.CharField(max_length=100, verbose_name="Prénom")
    last_name        = models.CharField(max_length=100, verbose_name="Nom")
    date_of_birth    = models.DateField(verbose_name="Date de naissance")
    gender           = models.CharField(max_length=10, choices=GENDER_CHOICES)
    cin              = models.CharField(max_length=20, unique=True, verbose_name="CIN")
    blood_group      = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    marital_status   = models.CharField(max_length=10, choices=MARITAL_CHOICES, blank=True)
    photo            = models.ImageField(upload_to='patients/photos/', blank=True, null=True)
    phone            = models.CharField(max_length=20, verbose_name="Téléphone")
    phone_alt        = models.CharField(max_length=20, blank=True)
    email            = models.EmailField(blank=True)
    address          = models.TextField(blank=True, verbose_name="Adresse")
    city             = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    insurance_name   = models.CharField(max_length=100, blank=True, verbose_name="Assurance")
    insurance_number = models.CharField(max_length=50, blank=True)
    file_number      = models.CharField(max_length=20, unique=True, blank=True, verbose_name="N° Dossier")

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        if not self.file_number:
            year = timezone.now().year
            count = Patient.objects.filter(file_number__startswith=f'P{year}').count()
            self.file_number = f'P{year}{count + 1:04d}'
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = timezone.now().date()
        b = self.date_of_birth
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    def __str__(self):
        return f"{self.full_name} ({self.file_number})"


class MedicalRecord(BaseModel):
    patient             = models.OneToOneField(Patient, on_delete=models.CASCADE,
                                               related_name='medical_record')
    allergies           = models.TextField(blank=True, verbose_name="Allergies")
    chronic_diseases    = models.TextField(blank=True, verbose_name="Maladies chroniques")
    past_surgeries      = models.TextField(blank=True, verbose_name="Antécédents chirurgicaux")
    family_history      = models.TextField(blank=True, verbose_name="Antécédents familiaux")
    current_medications = models.TextField(blank=True, verbose_name="Médicaments en cours")
    notes               = models.TextField(blank=True)

    class Meta:
        verbose_name = "Dossier médical"

    def __str__(self):
        return f"Dossier — {self.patient.full_name}"


class VitalSigns(models.Model):
    patient            = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                           related_name='vital_signs')
    weight             = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height             = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure_sys = models.IntegerField(null=True, blank=True, verbose_name="Tension sys.")
    blood_pressure_dia = models.IntegerField(null=True, blank=True, verbose_name="Tension dia.")
    temperature        = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    heart_rate         = models.IntegerField(null=True, blank=True, verbose_name="Fréq. cardiaque")
    measured_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-measured_at']

    @property
    def bmi(self):
        if self.weight and self.height and self.height > 0:
            h = float(self.height) / 100
            return round(float(self.weight) / h ** 2, 1)
        return None

    def __str__(self):
        return f"Constantes {self.patient.full_name}"