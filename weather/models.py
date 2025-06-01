from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class HistorySearchCityWeather(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_city = models.CharField(max_length=100)
    error = models.BooleanField(default=False, null=True, blank=True)
    date_search = models.DateTimeField()

    class Meta:
        verbose_name = "История поиска городов"
        verbose_name_plural = "История поиска городов"




class CountCity(models.Model):
    city = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Счетчик городов"
        verbose_name_plural = "Счетчики городов"