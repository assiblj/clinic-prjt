from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('',                                    views.consultation_list,   name='list'),
    path('create/',                             views.consultation_create, name='create'),
    path('<int:pk>/',                           views.consultation_detail, name='detail'),
    path('<int:consultation_pk>/prescription/', views.prescription_add,    name='prescription_add'),
    path('<int:consultation_pk>/lab/',          views.labrequest_add,      name='lab_add'),
]