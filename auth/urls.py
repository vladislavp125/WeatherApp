from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/registration/', views.user_register, name="registration")
]
