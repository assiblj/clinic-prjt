from django.db import models
from core.models import BaseModel
from accounts.models import CustomUser


class Specialty(models.Model):
    name        = models.CharField(max_length=100, unique=True, verbose_name="Spécialité")
    description = models.TextField(blank=True)
    icon        = models.CharField(max_length=50, blank=True, help_text="Classe Font Awesome")

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['name']

    def __str__(self):
        return self.name


class Doctor(BaseModel):
    user          = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                          related_name='doctor_profile', verbose_name="Utilisateur")
    specialty     = models.ForeignKey(Specialty, on_delete=models.SET_NULL,
                                       null=True, related_name='doctors', verbose_name="Spécialité")
    rpps_number   = models.CharField(max_length=20, blank=True, verbose_name="N° RPPS")
    bio           = models.TextField(blank=True, verbose_name="Biographie")
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2,
                                            default=0, verbose_name="Tarif consultation (MAD)")
    office_number = models.CharField(max_length=10, blank=True, verbose_name="N° Bureau")

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

    def __str__(self):
        return f"Dr. {self.user.full_name} — {self.specialty}"

    @property
    def full_name(self):
        return f"Dr. {self.user.full_name}"


class Nurse(BaseModel):
    user        = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                        related_name='nurse_profile', verbose_name="Utilisateur")
    department  = models.CharField(max_length=100, blank=True, verbose_name="Service")
    qualification = models.CharField(max_length=100, blank=True, verbose_name="Qualification")

    class Meta:
        verbose_name = "Infirmier/Infirmière"
        verbose_name_plural = "Infirmiers/Infirmières"

    def __str__(self):
        return self.user.full_name


class Schedule(models.Model):
    DAY_CHOICES = [
        (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'),
        (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche'),
    ]
    doctor     = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                    related_name='schedules', verbose_name="Médecin")
    day_of_week = models.IntegerField(choices=DAY_CHOICES, verbose_name="Jour")
    start_time  = models.TimeField(verbose_name="Heure début")
    end_time    = models.TimeField(verbose_name="Heure fin")
    slot_duration = models.IntegerField(default=30, verbose_name="Durée créneau (min)")
    is_active   = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Planning"
        unique_together = ['doctor', 'day_of_week']
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.doctor} — {self.get_day_of_week_display()} {self.start_time}–{self.end_time}"


class Leave(BaseModel):
    doctor      = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                     related_name='leaves', verbose_name="Médecin")
    start_date  = models.DateField(verbose_name="Date début")
    end_date    = models.DateField(verbose_name="Date fin")
    reason      = models.TextField(blank=True, verbose_name="Motif")

    class Meta:
        verbose_name = "Congé / Absence"
        verbose_name_plural = "Congés / Absences"

    def __str__(self):
        return f"{self.doctor} — {self.start_date} au {self.end_date}"