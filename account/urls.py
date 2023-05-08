from django.urls import path,include
from account.views import UserRegistrationView,PharmacyRegistrationView,UserLoginView,PharmacyLoginView,UserProfileView,UserPasswordResetView,UserChangePasswordView,SendPasswordResetEmailView

urlpatterns=[
  path('register/',UserRegistrationView.as_view(),name='register'),
  path('pharmacyRegister/',PharmacyRegistrationView.as_view(),name='PharmacyRegister'),
  path('login/',UserLoginView.as_view(),name='login'),
  path('pharmacyLogin/',PharmacyLoginView.as_view(),name='login'),
  path('profile/', UserProfileView.as_view(), name='profile'),
  path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
  path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
  path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),  
]