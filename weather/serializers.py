from rest_framework import serializers
from .models import CountCity


class CountCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountCity
        fields = "__all__"
