from django.db import models
from core.models import BaseModel
from patients.models import Patient
from consultations.models import Consultation


class MedicalAct(models.Model):
    name       = models.CharField(max_length=200, verbose_name="Acte médical")
    code       = models.CharField(max_length=20, unique=True, verbose_name="Code")
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Tarif (MAD)")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Acte médical"
        verbose_name_plural = "Actes médicaux"

    def __str__(self):
        return f"{self.code} — {self.name}"


class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('PENDING',   'En attente'),
        ('PAID',      'Payée'),
        ('PARTIAL',   'Partiellement payée'),
        ('CANCELLED', 'Annulée'),
    ]

    patient       = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                       related_name='invoices', verbose_name="Patient")
    consultation  = models.OneToOneField(Consultation, on_delete=models.SET_NULL,
                                          null=True, blank=True,
                                          related_name='invoice', verbose_name="Consultation")
    invoice_number = models.CharField(max_length=20, unique=True, blank=True,
                                       verbose_name="N° Facture")
    total_amount  = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=0, verbose_name="Montant total (MAD)")
    paid_amount   = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=0, verbose_name="Montant payé (MAD)")
    status        = models.CharField(max_length=15, choices=STATUS_CHOICES,
                                      default='PENDING', verbose_name="Statut")
    due_date      = models.DateField(null=True, blank=True, verbose_name="Date échéance")
    notes         = models.TextField(blank=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from django.utils import timezone
            year = timezone.now().year
            count = Invoice.objects.filter(
                invoice_number__startswith=f'F{year}').count()
            self.invoice_number = f'F{year}{count + 1:04d}'
        super().save(*args, **kwargs)

    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"Facture {self.invoice_number} — {self.patient}"


class InvoiceItem(models.Model):
    invoice     = models.ForeignKey(Invoice, on_delete=models.CASCADE,
                                     related_name='items', verbose_name="Facture")
    act         = models.ForeignKey(MedicalAct, on_delete=models.SET_NULL,
                                     null=True, blank=True, verbose_name="Acte")
    description = models.CharField(max_length=200, verbose_name="Description")
    quantity    = models.IntegerField(default=1, verbose_name="Quantité")
    unit_price  = models.DecimalField(max_digits=8, decimal_places=2,
                                       verbose_name="Prix unitaire (MAD)")

    class Meta:
        verbose_name = "Ligne de facture"

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} × {self.quantity}"


class Payment(models.Model):
    METHOD_CHOICES = [
        ('CASH',      'Espèces'),
        ('CARD',      'Carte bancaire'),
        ('TRANSFER',  'Virement'),
        ('INSURANCE', 'Assurance'),
        ('CHEQUE',    'Chèque'),
    ]

    invoice     = models.ForeignKey(Invoice, on_delete=models.CASCADE,
                                     related_name='payments', verbose_name="Facture")
    amount      = models.DecimalField(max_digits=10, decimal_places=2,
                                       verbose_name="Montant (MAD)")
    method      = models.CharField(max_length=15, choices=METHOD_CHOICES,
                                    verbose_name="Mode de paiement")
    paid_at     = models.DateTimeField(auto_now_add=True, verbose_name="Date paiement")
    reference   = models.CharField(max_length=100, blank=True,
                                    verbose_name="Référence / N° chèque")
    notes       = models.TextField(blank=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-paid_at']

    def __str__(self):
        return f"{self.amount} MAD — {self.get_method_display()} — {self.invoice}"