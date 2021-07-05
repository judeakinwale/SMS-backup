from django.urls import path
from .views import UserRegistrationView, StudentLoginView, StaffLoginView, BioDataView, HealthDataView


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('student/login/', StudentLoginView.as_view()),
    path('staff/login/', StaffLoginView.as_view()),
    path('biodata/', BioDataView.as_view()),
    path('healthdata/', HealthDataView.as_view()),
]