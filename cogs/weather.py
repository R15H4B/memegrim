from discord import Embed, Color
from discord.ext import commands
from discord.utils import get

from requests import get as rget
from os import environ
from datetime import datetime, timedelta
from sqlite3 import connect

class Weather(commands.Cog, name='Weather'):
    """
    Utilisable par tout le monde et permet d'avoir des prévisions météo.
    """
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_cast(city, forecast=False):
        if forecast:
            return rget(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&APPID={environ['WEATHER_TOKEN']}").json()
        data  = rget(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={environ['WEATHER_TOKEN']}").json()
        cleared_data = {
            'City': data['name'],
            'Hour': (datetime.utcfromtimestamp(data['dt']) + timedelta(hours=2)).strftime('%H:%M:%S'),
            'Weather forecast': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Feeling': f"{data['main']['feels_like']}°C",
            'Temperature min': f"{data['main']['temp_min']}°C",
            'Temperature max': f"{data['main']['temp_max']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']} Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h",
            'Sunset': (datetime.utcfromtimestamp(data['sys']['sunset']) + timedelta(hours=2)).strftime('%H:%M:%S'),
            'Sunrise': (datetime.utcfromtimestamp(data['sys']['sunrise']) + timedelta(hours=2)).strftime('%H:%M:%S'),
        }
        return cleared_data

    @commands.command(brief='weather [City]', description="Météo et prévisons sur 5 jours d'une ville")
    async def weather(self, ctx,  *, city):
        data = Weather.get_cast(city)
        embed = Embed(title=f":white_sun_small_cloud: Weather of {city} :", color=0x3498db)
        for key, value in data.items():
            embed.add_field(name=key, value=value)

        data = Weather.get_cast(city, True)
        days = {entry['dt_txt'][:10]: [] for entry in data['list']}
        for index, entry in enumerate(data['list']):
            days[entry['dt_txt'][:10]].append(f"{entry['dt_txt'][11:-3]} → {entry['weather'][0]['main']} - {entry['main']['temp']}°C\n")


def setup(bot):
    bot.add_cog(Weather(bot))