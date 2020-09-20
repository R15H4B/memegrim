from discord import Embed, Color
from discord.ext import commands
from discord.utils import get

from requests import get as rget
from os import environ
from datetime import datetime, timedelta
from sqlite3 import connect

class Weather(commands.Cog, name='Weather'):
    """
    Can be used by everyone and provides weather forecasts.
    """
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_cast(city, forecast=False):
        if forecast:
            return True, rget(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&APPID={environ['WEATHER_TOKEN']}").json()
        data  = rget(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={environ['WEATHER_TOKEN']}").json()
        try:
            cleared_data = {
                'City': data['name'],
                'Weather forecast': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
                'Temperature': f"{data['main']['temp']}°C",
                'Humidity': f"{data['main']['humidity']}%",
                'Pressure': f"{data['main']['pressure']} Pa",
                'Clouds': f"{data['clouds']['all']}%",
                'Wind': f"{data['wind']['speed']} km/h",
                'Sunset': (datetime.utcfromtimestamp(data['sys']['sunset']) + timedelta(hours=2)).strftime('%H:%M:%S'),
                'Sunrise': (datetime.utcfromtimestamp(data['sys']['sunrise']) + timedelta(hours=2)).strftime('%H:%M:%S'),
            }
            return True, cleared_data
        except Exception as e:
            wrong_data = {
                'Error': data['message'],
            }
            return False, wrong_data

    @commands.command(brief='weather [City]', description="Get weather forecast of a city")
    async def weather(self, ctx,  *, city):
        status, data = Weather.get_cast(city)
        if status: 
            embed = Embed(title=f":white_sun_small_cloud: Weather of {data['City']}:", color=0x1abc9c)
            for key, value in data.items():
                embed.add_field(name=key, value=value)
        else:
            embed = Embed(title=f"{data['Error']}!", color=0x1abc9c)

        # data = Weather.get_cast(city, True)
        # days = {entry['dt_txt'][:10]: [] for entry in data['list']}
        # for index, entry in enumerate(data['list']):
        #     days[entry['dt_txt'][:10]].append(f"{entry['dt_txt'][11:-3]} → {entry['weather'][0]['main']} - {entry['main']['temp']}°C\n")

        msg = await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather(bot))