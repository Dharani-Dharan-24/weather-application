import os
from dotenv import load_dotenv
import httpx
import asyncio
from .models import WeatherData, ForecastData
from datetime import datetime
from fastapi import HTTPException
load_dotenv()

class WeatherService:

    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.api_url = "https://api.openweathermap.org/data/2.5"

        if not self.api_key:
            raise ValueError("No API key found!")

    def test_connection(self):
        return f'API key loaded: {self.api_key[:8]}...' if self.api_key else "No API key!"

    async def get_current_weather(self, city: str):
        try:
            # Get coordinates first
            async with httpx.AsyncClient() as client:
                geo_response = await client.get(
                    f"{self.api_url}/weather",
                    params={
                        "q": city,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                if geo_response.status_code != 200:
                    error_data = geo_response.json()
                    raise HTTPException(
                        status_code=geo_response.status_code,
                        detail=error_data.get('message', 'Failed to fetch weather data')
                    )

                geo_data = geo_response.json()
                if not geo_data.get("coord"):
                    raise HTTPException(
                        status_code=404,
                        detail="City not found"
                    )

                # Get hourly forecast using coordinates
                forecast_response = await client.get(
                    f"{self.api_url}/forecast",
                    params={
                        "lat": geo_data["coord"]["lat"],
                        "lon": geo_data["coord"]["lon"],
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                if forecast_response.status_code != 200:
                    raise HTTPException(
                        status_code=forecast_response.status_code,
                        detail="Failed to fetch forecast data"
                    )

                forecast_data = forecast_response.json()

                # Process current weather
                try:
                    current_weather = WeatherData(
                        city=geo_data["name"],
                        country=geo_data["sys"]["country"],
                        temperature=geo_data["main"]["temp"],
                        feels_like=geo_data["main"]["feels_like"],
                        humidity=geo_data["main"]["humidity"],
                        pressure=geo_data["main"]["pressure"],
                        description=geo_data["weather"][0]["description"],
                        icon=geo_data["weather"][0]["icon"],
                        wind_speed=geo_data["wind"]["speed"],
                        timestamp=datetime.utcfromtimestamp(geo_data["dt"])
                    )
                except KeyError as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Invalid weather data format: missing {str(e)}"
                    )

                # Process hourly forecast (next 24 hours)
                hourly_forecast = []
                try:
                    for hour in forecast_data["list"][:8]:  # 8 entries = 24 hours (3-hour intervals)
                        forecast = ForecastData(
                            date=datetime.utcfromtimestamp(hour["dt"]).strftime("%I %p"),  # Hour in 12-hour format
                            temperature_max=hour["main"]["temp_max"],
                            temperature_min=hour["main"]["temp_min"],
                            description=hour["weather"][0]["description"],
                            icon=hour["weather"][0]["icon"]
                        )
                        hourly_forecast.append(forecast)
                except (KeyError, IndexError) as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Invalid forecast data format: {str(e)}"
                    )

                return {
                    "city": current_weather.city,
                    "country": current_weather.country,
                    "temperature": round(current_weather.temperature),
                    "feels_like": round(current_weather.feels_like),
                    "humidity": current_weather.humidity,
                    "pressure": current_weather.pressure,
                    "description": current_weather.description,
                    "icon": current_weather.icon,
                    "wind_speed": current_weather.wind_speed,
                    "forecast": hourly_forecast
                }

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}"
            )
