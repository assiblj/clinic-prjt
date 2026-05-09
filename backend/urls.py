"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('patients/', include('patients.urls', namespace='patients')),
    path('dashboard/', include('core.urls', namespace='core')),
    path('staff/',         include('staff.urls',         namespace='staff')),
    path('appointments/',  include('appointments.urls',  namespace='appointments')),
    path('consultations/', include('consultations.urls', namespace='consultations')),
    path('billing/',       include('billing.urls',       namespace='billing')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)