import os

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
AQI_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
BARK_URL = "https://api.day.app"

LAT = 35.21
LON = 113.29

API_KEY = os.environ.get("API_KEY")
BARK_KEY = os.environ.get("BARK_KEY")

# 阈值
PRESSURE_LOW = 990
PRESSURE_RATE_THRESHOLD = 1.0

WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0
NE_MIN = 20
NE_MAX = 100

AQI_THRESHOLD = 4  # ⚠️ OpenWeather是1~5等级（非真实AQI）

STATE_FILE = "fusion_state.txt"
PRESSURE_FILE = "pressure_state.txt"
