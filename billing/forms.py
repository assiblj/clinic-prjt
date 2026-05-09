from django import forms
from .models import Invoice, InvoiceItem, Payment


class InvoiceForm(forms.ModelForm):
    class Meta:
        model  = Invoice
        fields = ['patient', 'consultation', 'due_date', 'notes']
        widgets = {
            'patient':      forms.Select(attrs={'class': 'form-select'}),
            'consultation': forms.Select(attrs={'class': 'form-select'}),
            'due_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes':        forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model  = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity':    forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price':  forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    # Champs carte bancaire
    card_number  = forms.CharField(
        max_length=19, required=False, label="Numéro de carte",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'XXXX XXXX XXXX XXXX',
            'maxlength': '19', 'id': 'card_number'
        })
    )
    card_holder  = forms.CharField(
        max_length=100, required=False, label="Nom sur la carte",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'ASSIA BENALI',
            'id': 'card_holder'
        })
    )
    card_expiry  = forms.CharField(
        max_length=5, required=False, label="Date d'expiration",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'MM/YY',
            'maxlength': '5', 'id': 'card_expiry'
        })
    )
    card_cvv     = forms.CharField(
        max_length=4, required=False, label="CVV",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': '***',
            'maxlength': '4', 'id': 'card_cvv'
        })
    )
    # Champ chèque
    cheque_number = forms.CharField(
        max_length=50, required=False, label="Numéro de chèque",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'N° du chèque',
            'id': 'cheque_number'
        })
    )
    cheque_bank = forms.CharField(
        max_length=100, required=False, label="Banque émettrice",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Nom de la banque',
            'id': 'cheque_bank'
        })
    )
    # Champ virement
    transfer_ref = forms.CharField(
        max_length=100, required=False, label="Référence virement",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Référence du virement',
            'id': 'transfer_ref'
        })
    )

    class Meta:
        model  = Payment
        fields = ['amount', 'method', 'reference', 'notes']
        widgets = {
            'amount':    forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount'}),
            'method':    forms.Select(attrs={'class': 'form-select', 'id': 'payment_method',
                                             'onchange': 'showPaymentFields()'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'notes':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }