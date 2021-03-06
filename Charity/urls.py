"""Charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from charity_donation.views import LandingPage, AddDonation, Login, Register, Logout, UserProfile, third_step_filter, \
    FormConfirmation, is_taken_change, EditUser, ChangePassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('add_donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('user_profile/', UserProfile.as_view(), name='user-profile'),
    path('third_step_filter/', third_step_filter, name='third-step-filter'),
    path('form_confirmation/', FormConfirmation.as_view(), name='form-confirmation'),
    path('is_taken_change/', is_taken_change, name='is-taken-change'),
    path('edit_user/', EditUser.as_view(), name='edit-user'),
    path('change_password/', ChangePassword.as_view(), name='change-password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
