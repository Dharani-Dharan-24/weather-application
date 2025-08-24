# Weather Application

A modern web application that provides real-time weather information using FastAPI and OpenWeather API.

## Features

- Real-time weather data display
- City-based weather search
- Displays comprehensive weather information including:
  - Temperature
  - Feels like temperature
  - Humidity
  - Pressure
  - Weather description
  - Wind speed
  - Country information

## Technology Stack

- Backend: FastAPI (Python)
- Frontend: HTML, JavaScript
- Template Engine: Jinja2
- API: OpenWeather API

## Prerequisites

- Python 3.8+
- FastAPI
- OpenWeather API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dharani-Dharan-24/weather-application
cd weather_application
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenWeather API key:
   - Sign up at [OpenWeather](https://openweathermap.org/api)
   - Get your API key
   - Set it as an environment variable or in your configuration

## Project Structure

```
weather_application/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and routes
│   ├── models.py         # Data models
│   └── weather_service.py # Weather service logic
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
│   ├── base.html
│   └── index.html
├── requirements.txt
└── README.md
```

## Running the Application

1. Start the FastAPI server:
```bash
fastapi dev main.py
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

## Usage

1. Enter a city name in the search box
2. Click the search button or press Enter
3. View the detailed weather information for the specified city

## Features in Development

- Hourly weather forecasts
- Location pinning
- Country selection
- Enhanced UI animations and transitions
- Interactive backgrounds

## License

This project is licensed under the MIT License - see the LICENSE file for details.
