from django.urls import path
from . import views


urlpatterns = [
    path('main_page/', views.main_page, name="anime_page")
]
