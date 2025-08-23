import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.weather_service import WeatherService
weather_service = WeatherService()

app = FastAPI(title="Weather Application")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
templates = Jinja2Templates(directory=os.path.join(PROJECT_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_DIR, "static")), name="static")


@app.get('/weather', response_class=HTMLResponse)
async def get_weather(request: Request, city: str, country: str = None):
    try:
        search_query = f"{city},{country}" if country else city
        weather = await weather_service.get_current_weather(search_query)
        return templates.TemplateResponse('index.html', {
            "request": request,
            "weather": weather,
            "error": None
        })
    except HTTPException as he:
        return templates.TemplateResponse('index.html', {
            "request": request,
            "weather": None,
            "error": he.detail
        })
    except Exception as e:
        return templates.TemplateResponse('index.html', {
            "request": request,
            "weather": None,
            "error": "An unexpected error occurred. Please try again later."
        })

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login():
    return {"message": "Login!"}