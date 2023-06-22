from django.http import JsonResponse
import requests
from decouple import config


def get_weather(request):
    API_KEY = config("WEATHER_API_KEY")
    SEOUL_URL = (
        f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
    )

    response = requests.get(SEOUL_URL)
    data = response.json()

    return JsonResponse(data)
