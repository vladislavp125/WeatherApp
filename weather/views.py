from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CountCitySerializer
from .models import HistorySearchCityWeather, CountCity
from datetime import datetime
import asyncio
import httpx


async def get_weather_data(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    async with httpx.AsyncClient() as client:
        geo_resp = await client.get(url, params={"name": city, "count": 1})
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {"error": "Город не найден"}

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_resp = await client.get(weather_url, params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        })
        return weather_resp.json()


def index(request):
    user = request.user
    city = None
    forecast = None

    history = HistorySearchCityWeather.objects.filter(user=request.user, error=False) \
        .order_by('search_city') \
        .values_list('search_city', flat=True) \
        .distinct()

    if request.method == "POST":
        city = request.POST.get("city")
        forecast = asyncio.run(get_weather_data(city))

        if "error" in forecast:
            HistorySearchCityWeather.objects.create(
                search_city=city,
                user=user,
                error=True,
                date_search=datetime.now()
            )
        else:
            HistorySearchCityWeather.objects.create(
                search_city=city,
                user=user,
                date_search=datetime.now()
            )

        count_city = CountCity.objects.filter(city=city).first()
        if count_city:
            count_city.count += 1
            count_city.save()
        else:
            CountCity.objects.create(
                city=city,
                count=1,
                user=user
            )

    return render(request, "index.html", {
        "city": city,
        "forecast": forecast,
        "history": history
    })


class CityCountViewSet(viewsets.ModelViewSet):
    queryset = CountCity.objects.all()
    serializer_class = CountCitySerializer
