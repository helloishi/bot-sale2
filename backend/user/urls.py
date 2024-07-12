from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change/password/', PasswordChangeView.as_view(), name='change-password'),
    path('change/phone/', MobilePhoneChangeView.as_view(), name='change-mobile-phone'),
    path('change/username/', UsernameChangeView.as_view(), name='change-username'),
]
