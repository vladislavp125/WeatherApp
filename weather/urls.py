from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("countcity", views.CityCountViewSet)

urlpatterns = [
    path('main_page/', views.index, name="index"),
    path('api/', include(router.urls)),
]
