from django.urls import path
from .views import RegisterView, VerifyView, CompleteRegistrationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('complete-registration/', CompleteRegistrationView.as_view(), name='complete_registration'),
]
