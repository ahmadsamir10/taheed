from django.urls import path
from .views import RegisterView, VerifyView, CompleteRegistrationView, MotorcycleInfoView, ClientDashbboardView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('complete-registration/', CompleteRegistrationView.as_view(), name='complete_registration'),
    path('fetch-motorcycle-info/', MotorcycleInfoView.as_view(), name='fetch-motorcycle-info'),
    
    # dahsboard
    path('dahsboard/', ClientDashbboardView.as_view(), name='dahsboard'),
    
]
