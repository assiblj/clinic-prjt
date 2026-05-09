from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('',                    views.appointment_list,    name='list'),
    path('create/',             views.appointment_create,  name='create'),
    path('<int:pk>/edit/',      views.appointment_edit,    name='edit'),
    path('<int:pk>/cancel/',    views.appointment_cancel,  name='cancel'),
    path('<int:pk>/confirm/',   views.appointment_confirm, name='confirm'),
]