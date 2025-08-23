from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WeatherData(BaseModel):

    city : str
    country : str
    temperature : float
    feels_like: float
    humidity : int
    pressure : float
    description : str
    icon : str
    wind_speed : float
    timestamp : datetime

class ForecastData(BaseModel):

    date: str
    temperature_max: float
    temperature_min: float
    description: str
    icon: str

class WeatherResponse(BaseModel):
    current: WeatherData
    forecast: List[ForecastData]
    error: Optional[str] = None


