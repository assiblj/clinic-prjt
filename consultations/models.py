from django.db import models
from core.models import BaseModel
from patients.models import Patient
from staff.models import Doctor
from appointments.models import Appointment


class Consultation(BaseModel):
    patient       = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                       related_name='consultations', verbose_name="Patient")
    doctor        = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                       related_name='consultations', verbose_name="Médecin")
    appointment   = models.OneToOneField(Appointment, on_delete=models.SET_NULL,
                                          null=True, blank=True,
                                          related_name='consultation', verbose_name="RDV")
    date          = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    motif         = models.TextField(verbose_name="Motif")
    clinical_exam = models.TextField(blank=True, verbose_name="Examen clinique")
    diagnosis     = models.TextField(verbose_name="Diagnostic")
    treatment     = models.TextField(blank=True, verbose_name="Traitement prescrit")
    notes         = models.TextField(blank=True, verbose_name="Notes")
    follow_up_date = models.DateField(null=True, blank=True, verbose_name="Date suivi")

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"
        ordering = ['-date']

    def __str__(self):
        return f"Consultation — {self.patient} — {self.date:%d/%m/%Y}"


class Prescription(BaseModel):
    consultation  = models.OneToOneField(Consultation, on_delete=models.CASCADE,
                                          related_name='prescription',
                                          verbose_name="Consultation")
    patient       = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                       related_name='prescriptions', verbose_name="Patient")
    doctor        = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                       related_name='prescriptions', verbose_name="Médecin")
    notes         = models.TextField(blank=True, verbose_name="Instructions générales")
    valid_until   = models.DateField(null=True, blank=True, verbose_name="Valide jusqu'au")

    class Meta:
        verbose_name = "Ordonnance"
        verbose_name_plural = "Ordonnances"

    def __str__(self):
        return f"Ordonnance — {self.patient} — {self.created_at:%d/%m/%Y}"


class PrescriptionItem(models.Model):
    prescription  = models.ForeignKey(Prescription, on_delete=models.CASCADE,
                                       related_name='items', verbose_name="Ordonnance")
    medication_name = models.CharField(max_length=200, verbose_name="Médicament")
    dosage        = models.CharField(max_length=100, verbose_name="Dosage")
    frequency     = models.CharField(max_length=100, verbose_name="Fréquence")
    duration      = models.CharField(max_length=100, verbose_name="Durée")
    instructions  = models.TextField(blank=True, verbose_name="Instructions")

    class Meta:
        verbose_name = "Ligne d'ordonnance"

    def __str__(self):
        return f"{self.medication_name} — {self.dosage}"


class LabRequest(BaseModel):
    TYPE_CHOICES = [
        ('BLOOD',    'Analyse sanguine'),
        ('URINE',    'Analyse urinaire'),
        ('XRAY',     'Radiographie'),
        ('ECHO',     'Échographie'),
        ('SCAN',     'Scanner'),
        ('MRI',      'IRM'),
        ('OTHER',    'Autre'),
    ]
    STATUS_CHOICES = [
        ('PENDING',  'En attente'),
        ('DONE',     'Réalisé'),
        ('CANCELLED','Annulé'),
    ]

    consultation  = models.ForeignKey(Consultation, on_delete=models.CASCADE,
                                       related_name='lab_requests', verbose_name="Consultation")
    patient       = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                       related_name='lab_requests', verbose_name="Patient")
    type          = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    description   = models.TextField(verbose_name="Description / Examens demandés")
    status        = models.CharField(max_length=15, choices=STATUS_CHOICES,
                                      default='PENDING', verbose_name="Statut")
    result        = models.TextField(blank=True, verbose_name="Résultats")
    result_file   = models.FileField(upload_to='lab_results/', blank=True, null=True,
                                      verbose_name="Fichier résultat")

    class Meta:
        verbose_name = "Demande d'examen"
        verbose_name_plural = "Demandes d'examens"

    def __str__(self):
        return f"{self.get_type_display()} — {self.patient}"