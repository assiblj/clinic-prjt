from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('',                        views.invoice_list,   name='list'),
    path('create/',                 views.invoice_create, name='create'),
    path('<int:pk>/',               views.invoice_detail, name='detail'),
    path('<int:invoice_pk>/pay/',   views.payment_add,    name='payment_add'),
]