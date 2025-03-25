
import asyncio
import bips
import brain
import eyes
from open_meteo import OpenMeteo
from geopy.geocoders import Nominatim
from open_meteo.models import DailyParameters, HourlyParameters
import re
from datetime import datetime, timedelta
import time
from word2number import w2n


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
LONGITUDE = 0.34

INTENTS = [
    "WEATHER_NOW",
    "WEATHER_CITY",
    "WEATHER_AT",
    "WEATHER_WEEKEND",
    "WEATHER_TOMORROW"
]

open_street_map = Nominatim(user_agent="luxy")

def to_number(number):
    if number.isDigit():
        return int(number)
    else:
        return w2n.word_to_num(number)

def convert_time(time):
    time = time.strip().replace(" ", "").replace('min', '').replace('.', '')
    time = re.sub(r"([0-9]+)([^0-9])", r"\1 \2", time)
    time = re.sub(r"([^0-9])([0-9]+)", r"\1 \2", time)
    match time.split():
        case ["half", "past", hour]:
            return [to_number(hour), 30]
        case [min, "past", hour]:
            return [to_number(hour), to_number(min)]
        case [min, "to", hour]:
            min = 60 - to_number(min)
            return [to_number(hour), min]
        case [hour,":",min,"am"]:
            return [to_number(hour), to_number(min)]
        case [hour, ":", min, "pm"]:
            hour = to_number(hour) + 12
            return [hour, to_number(min)]
        case [hour, ":", min]:
            return [to_number(hour), to_number(min)]
        case [hour, "h", min]:
            return [to_number(hour), to_number(min)]
        case [hour, "am"]:
            return [to_number(hour), 0]
        case [hour, "pm"]:
            hour = to_number(hour) + 12
            return [hour, 0]
        case _:
            return to_number(time)
        
def find_time(request):
    return (brain.think("What time is mentioned there ?", request))
        
def extract_time(request):
    request = request.replace('?', '')
    score = 1
    if(re.match(r'.*[0-9]+.*', request) == None):
        score, _, _, time = (brain.think("What hour does the question '{0}' best correspond to?".format(request), "The morning is at 7am, Noon is at 12am, Afternoon is at 3pm, tonight is at 7pm, Evening is at 9pm")).values()
    else:
        score, _, _, time = find_time(request).values()
    time = convert_time(time)
    return [time, score]

async def weather_at(request, latitude = LATITUDE, longitude = LONGITUDE): 
    eyes.thinking(True)
    time, score = extract_time(request)
    print("Fetching the weather at {0} with confidence {1}".format(time, score))

    hour, min = time
    if(min >= 30):
        hour = (hour + 1) % 24
        
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=latitude,
            longitude=longitude,
            hourly=[
                HourlyParameters.TEMPERATURE_2M,
                HourlyParameters.WEATHER_CODE,
                HourlyParameters.WIND_SPEED_10M
            ],
        )
    eyes.thinking(False)
    index = next(idx for idx, date in enumerate(forecast.hourly.time) if date.hour == hour)
    weather_code = forecast.hourly.weather_code[index]
    temperature = forecast.hourly.temperature_2m[index]
    wind = forecast.hourly.wind_speed_10m[index]
    bips.say("Sky: <prosody pitch='120'>{0}</prosody>;".format(weather_codes[weather_code]))
    bips.say("Temperature: <prosody pitch='120'>{0}</prosody>;".format(temperature))
    bips.say("Wind: <prosody pitch='120'>{0}</prosody>".format(wind))
    return score

async def weather_date(date, latitude = LATITUDE, longitude = LONGITUDE):
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=latitude,
            longitude=longitude,
            daily=[
                DailyParameters.TEMPERATURE_2M_MAX,
                DailyParameters.TEMPERATURE_2M_MIN,
                DailyParameters.WEATHER_CODE,
            ],
        )
    index = next(idx for idx, d in enumerate(forecast.daily.time) if d.day == date.day)
    weather_code = forecast.daily.weathercode[index]
    temperature_min = forecast.daily.temperature_2m_min[index]
    temperature_max = forecast.daily.temperature_2m_max[index]
    bips.say("Sky: <prosody pitch='120'>{0}</prosody>;".format(weather_codes[weather_code]))
    bips.say("Min temp: <prosody pitch='120'>{0}</prosody>;".format(temperature_min))
    bips.say("Max temp: <prosody pitch='120'>{0}</prosody>;".format(temperature_max))
    return 1

async def weather_tomorrow(latitude = LATITUDE, longitude = LONGITUDE):
    date = datetime.today()
    date += timedelta(days=1)
    return await weather_date(date, latitude, longitude)

async def weather_weekend(latitude = LATITUDE, longitude = LONGITUDE):
    date = datetime.today()
    t = timedelta((12 - date.weekday()) % 7)
    saturday = date + t
    sunday = saturday + timedelta(days=1)
    bips.say("Saturday;")
    await weather_date(saturday, latitude, longitude)
    time.sleep(0.5)
    bips.say("Sunday;")
    await weather_date(sunday, latitude, longitude)
    return 1

async def weather_now(latitude = LATITUDE, longitude = LONGITUDE):
    eyes.thinking(True)
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=latitude,
            longitude=longitude,
            current_weather=True
        )
    eyes.thinking(False)
    bips.say("Sky: <prosody pitch='120'>{0}</prosody>;".format(weather_codes[forecast.current_weather.weather_code]))
    bips.say("Temperature: <prosody pitch='120'>{0}</prosody>;".format(forecast.current_weather.temperature))
    bips.say("Wind: <prosody pitch='120'>{0}</prosody>".format(forecast.current_weather.wind_speed))
    return 1

async def weather_city(request):
    eyes.thinking(True)
    placeScore, _, _, city = brain.think("What city or place is mentioned there ?", request).values()
    location = open_street_map.geocode(city).raw
    print("Fetching the weather in {0} with confidence {1}".format(city, placeScore))
    weatherScore = await weather_now(location["lat"], location["lon"])
    eyes.thinking(False)
    return placeScore * weatherScore


def main(intent, request):
    match intent:
        case "WEATHER_AT":
            return asyncio.run(weather_at(request))
        case "WEATHER_NOW":
            return asyncio.run(weather_now())
        case "WEATHER_TOMORROW":
            return asyncio.run(weather_tomorrow())
        case "WEATHER_WEEKEND":
            return asyncio.run(weather_weekend(request))
        case "WEATHER_CITY":
            return asyncio.run(weather_city(request))
        case _:
            return 0


