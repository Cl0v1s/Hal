import brain

INTENTS = [
    "WEATHER_HERE",
    "WEATHER_SPECIFIC_PLACE",
    "WEATHER_CITY",
    "WEATHER_TODAY",
    "WEATHER_WEEKEND",
    "WEATHER_TOMORROW",
    "WEATHER_SPECIFIC_DATE"
]

def main(intent, request):
    print(intent)
    print(request)
    pass