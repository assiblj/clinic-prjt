from django.db import models
from django.utils import timezone
from core.models import BaseModel
from patients.models import Patient
from staff.models import Doctor


class Appointment(BaseModel):
    STATUS_CHOICES = [
        ('PENDING',    'En attente'),
        ('CONFIRMED',  'Confirmé'),
        ('CANCELLED',  'Annulé'),
        ('COMPLETED',  'Honoré'),
        ('NO_SHOW',    'Absent'),
    ]
    TYPE_CHOICES = [
        ('CONSULTATION', 'Consultation'),
        ('FOLLOWUP',     'Suivi'),
        ('EMERGENCY',    'Urgence'),
        ('CHECKUP',      'Bilan'),
    ]

    patient      = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                      related_name='appointments', verbose_name="Patient")
    doctor       = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                      related_name='appointments', verbose_name="Médecin")
    date_time    = models.DateTimeField(verbose_name="Date et heure")
    duration     = models.IntegerField(default=30, verbose_name="Durée (min)")
    motif        = models.TextField(verbose_name="Motif de consultation")
    type         = models.CharField(max_length=20, choices=TYPE_CHOICES,
                                     default='CONSULTATION', verbose_name="Type")
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES,
                                     default='PENDING', verbose_name="Statut")
    notes        = models.TextField(blank=True, verbose_name="Notes")
    reminder_sent = models.BooleanField(default=False, verbose_name="Rappel envoyé")

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['-date_time']

    def __str__(self):
        return f"{self.patient} — Dr.{self.doctor} — {self.date_time:%d/%m/%Y %H:%M}"

    def confirm(self):
        self.status = 'CONFIRMED'
        self.save(update_fields=['status', 'updated_at'])

    def cancel(self):
        self.status = 'CANCELLED'
        self.save(update_fields=['status', 'updated_at'])

    def complete(self):
        self.status = 'COMPLETED'
        self.save(update_fields=['status', 'updated_at'])

    @property
    def is_upcoming(self):
        return self.date_time > timezone.now() and self.status in ['PENDING', 'CONFIRMED']


class TimeSlot(models.Model):
    doctor      = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                     related_name='time_slots')
    date        = models.DateField(verbose_name="Date")
    start_time  = models.TimeField(verbose_name="Heure début")
    end_time    = models.TimeField(verbose_name="Heure fin")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Créneau"
        unique_together = ['doctor', 'date', 'start_time']
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor} — {self.date} {self.start_time}"