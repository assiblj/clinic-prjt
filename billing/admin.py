from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment, MedicalAct

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['paid_at']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display  = ['invoice_number', 'patient', 'total_amount',
                      'paid_amount', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['patient__first_name', 'invoice_number']
    inlines       = [InvoiceItemInline, PaymentInline]

@admin.register(MedicalAct)
class MedicalActAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'base_price']