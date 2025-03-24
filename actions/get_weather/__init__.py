
import asyncio
import bips
import brain
import eyes
from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters
import re

weather_codes = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow fall",
    73: "Moderate Snow fall",
    75: "Heavy Snow fall",
    77: "Snow grains",
    80: "Slight Rain showers",
    81: "Moderate Rain showers",
    82: "Violent Rain showers",
    85: "slight Snow showers",
    86: "heavy Snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

LATITUDE = 44.5
LONGITUE = 0.34

INTENTS = [
    "WEATHER_NOW",
    "WEATHER_SPECIFIC_PLACE",
    "WEATHER_CITY",
    "WEATHER_AT",
    "WEATHER_WEEKEND",
    "WEATHER_TOMORROW",
    "WEATHER_SPECIFIC_DATE"
]

def convert_time(time):
    time = time.strip().replace(" ", "").replace('min', '').replace('.', '')
    time = re.sub(r"([0-9]+)([^0-9])", r"\1 \2", time)
    time = re.sub(r"([^0-9])([0-9]+)", r"\1 \2", time)
    match time.split():
        case ["half", "past", hour]:
            return [int(hour), 30]
        case [min, "past", hour]:
            return [int(hour), int(min)]
        case [min, "to", hour]:
            min = 60 - int(min)
            return [int(hour), min]
        case [hour,":",min,"am"]:
            return [int(hour), int(min)]
        case [hour, ":", min, "pm"]:
            hour = int(hour) + 12
            return [hour, int(min)]
        case [hour, ":", min]:
            return [int(hour), int(min)]
        case [hour, "h", min]:
            return [int(hour), int(min)]
        case [hour, "am"]:
            return [int(hour), 0]
        case [hour, "pm"]:
            hour = int(hour) + 12
            return [hour, 0]
        case _:
            return None
        
def extract_time(request):
    request = request.replace('?', '')
    score = 1
    if(re.match(r'.*[0-9]+.*', request) == None):
        score, _, _, time = (brain.think("What hour does the question '{0}' best correspond to?".format(request), "The morning is at 7am, Noon is at 12am, Afternoon is at 3pm, tonight is at 7pm, Evening is at 9pm")).values()
    else:
        score, _, _, time = (brain.think("What time is mentioned there ?", request)).values()
    time = convert_time(time)
    return [time, score]

def weather_at(request): 
    time, score = extract_time(request)
    print("Fetching the weather at {0} with confidence {1}".format(time, score))

        
    # async with OpenMeteo() as open_meteo:
    #     forecast = await open_meteo.forecast(
    #         latitude=LATITUDE,
    #         longitude=LONGITUE,
    #         hourly=[
    #             HourlyParameters.TEMPERATURE_2M,
    #         ],
    #     )

async def weather_now():
    eyes.thinking(True)
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=LATITUDE,
            longitude=LONGITUE,
            current_weather=True
        )
    eyes.thinking(False)
    bips.say("Sky: <prosody pitch='120'>{0}</prosody>;".format(weather_codes[forecast.current_weather.weather_code]))
    bips.say("Temperature: <prosody pitch='120'>{0}</prosody>;".format(forecast.current_weather.temperature))
    bips.say("Wind: <prosody pitch='120'>{0}</prosody>".format(forecast.current_weather.wind_speed))

def main(intent, request):
    match intent:
        case "WEATHER_AT":
            asyncio.run(weather_at(request))
        case "WEATHER_NOW":
            asyncio.run(weather_now())
        case _:
            pass
    pass


