from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceItem, Payment
from .forms import InvoiceForm, InvoiceItemForm, PaymentForm


@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(
        is_active=True
    ).select_related('patient').order_by('-created_at')
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, pk):
    invoice  = get_object_or_404(Invoice, pk=pk)
    items    = invoice.items.all()
    payments = invoice.payments.all()
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice, 'items': items, 'payments': payments
    })


@login_required
def invoice_create(request):
    ItemFormSet = inlineformset_factory(
        Invoice, InvoiceItem,
        form=InvoiceItemForm, extra=3, can_delete=True
    )
    form = InvoiceForm(request.POST or None)
    formset = ItemFormSet(request.POST or None)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        invoice = form.save(commit=False)
        invoice.created_by = request.user
        invoice.save()
        formset.instance = invoice
        items = formset.save()
        # Calcul du total
        invoice.total_amount = sum(i.total for i in invoice.items.all())
        invoice.save(update_fields=['total_amount'])
        messages.success(request, f'Facture {invoice.invoice_number} créée.')
        return redirect('billing:detail', pk=invoice.pk)
    return render(request, 'billing/invoice_form.html', {
        'form': form, 'formset': formset, 'title': 'Nouvelle facture'
    })


@login_required
def payment_add(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    form    = PaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        payment = form.save(commit=False)
        payment.invoice = invoice
        payment.save()
        # Mise à jour montant payé
        invoice.paid_amount = sum(p.amount for p in invoice.payments.all())
        if invoice.paid_amount >= invoice.total_amount:
            invoice.status = 'PAID'
        elif invoice.paid_amount > 0:
            invoice.status = 'PARTIAL'
        invoice.save(update_fields=['paid_amount', 'status'])
        messages.success(request, f'Paiement de {payment.amount} MAD enregistré.')
        return redirect('billing:detail', pk=invoice_pk)
    return render(request, 'billing/payment_form.html', {
        'form': form, 'invoice': invoice
    })




