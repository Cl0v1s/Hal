
import asyncio
import os
from datetime import datetime
from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters

LATITUDE = 44.5
LONGITUE = 0.34

INTENTS = [
    "WEATHER_HERE",
    "WEATHER_SPECIFIC_PLACE",
    "WEATHER_CITY",
    "WEATHER_TODAY",
    "WEATHER_WEEKEND",
    "WEATHER_TOMORROW",
    "WEATHER_SPECIFIC_DATE"
]


async def weather_today(): 
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=LATITUDE,
            longitude=LONGITUE,
            hourly=[
                HourlyParameters.TEMPERATURE_2M,
            ],
        )
        print(forecast)

async def weather_here():
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=LATITUDE,
            longitude=LONGITUE,
            current_weather=True
        )

        # with open('here.json', 'w') as f:
        #     json.dump(forecast.to_json(), f)
        # now = datetime.now()
        # hour = now.hour
        # if now.minute >= 30 and hour + 1 < 24:
        #     hour += 1
        # index = [t.hour for t in forecast.hourly.time].index(hour)
        # print(forecast.hourly.temperature_2m[index])
        os.system('espeak "Il fait {0} degrès et le vent souffle à ${0} kM/h" 2>/dev/null'.format(forecast.current_weather.temperature, forecast.current_weather.wind_speed))


def main(intent, request):
    match intent:
        case "WEATHER_TODAY":
            asyncio.run(weather_today())
        case "WEATHER_HERE":
            asyncio.run(weather_here())
        case _:
            pass
    pass