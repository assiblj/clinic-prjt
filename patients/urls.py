from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('',                      views.patient_list,        name='list'),
    path('create/',               views.patient_create,      name='create'),
    path('<int:pk>/',             views.patient_detail,      name='detail'),
    path('<int:pk>/edit/',        views.patient_edit,        name='edit'),
    path('<int:pk>/delete/',      views.patient_delete,      name='delete'),
    path('<int:pk>/record/',      views.medical_record_edit, name='record_edit'),
    path('<int:pk>/vitals/add/',  views.vital_signs_add,     name='vitals_add'),
]