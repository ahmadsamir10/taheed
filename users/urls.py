from django.urls import path
from .views import RegisterView, VerifyView, CompleteRegistrationView, MotorcycleInfoView, ClientDashbboardView, AddMotorcyclesView, LoginToDashboardView, RequestToLoginView

namespace = "users"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('complete-registration/', CompleteRegistrationView.as_view(), name='complete_registration'),
    path('fetch-motorcycle-info/', MotorcycleInfoView.as_view(), name='fetch-motorcycle-info'),
    
    # dahsboard
    path('dahsboard/login/', LoginToDashboardView.as_view(), name='login-to-dashboard'),
    path('dahsboard/login/request/', RequestToLoginView.as_view(), name='request-to-login'),
    path('dahsboard/', ClientDashbboardView.as_view(), name='dahsboard'),
    path('add-motorcyles/', AddMotorcyclesView.as_view(), name='add-motorcyles')
    
]
