from django.urls import path
from .views import RegisterView, VerifyView, CompleteRegistrationView, MotorcycleInfoView, ClientDashbboardView, AddMotorcyclesView, LoginToDashboardView, RequestToLoginView

namespace = "users"

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('users/verify/', VerifyView.as_view(), name='verify'),
    path('users/complete-registration/', CompleteRegistrationView.as_view(), name='complete_registration'),
    path('users/fetch-motorcycle-info/', MotorcycleInfoView.as_view(), name='fetch-motorcycle-info'),
    
    # dahsboard
    path('users/dahsboard/login/', LoginToDashboardView.as_view(), name='login-to-dashboard'),
    path('users/dahsboard/login/request/', RequestToLoginView.as_view(), name='request-to-login'),
    path('users/dahsboard/', ClientDashbboardView.as_view(), name='dahsboard'),
    path('users/add-motorcyles/', AddMotorcyclesView.as_view(), name='add-motorcyles')
    
]
