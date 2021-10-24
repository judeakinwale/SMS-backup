from django.core.mail import send_mail
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .utils import send_sample_email

app_name = 'core'

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path('mail/', send_sample_email, name='send_mail')
]
