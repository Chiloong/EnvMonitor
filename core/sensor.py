import requests
from config import *

QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
WAQI_API = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"

def fetch_all():
    url = f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}"
    w = requests.get(url, timeout=10).json()

    now = w["now"]

    aqi_url = WAQI_API.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
    a = requests.get(aqi_url, timeout=10).json()

    return {
        "pressure": float(now.get("pressure", 0)),
        "humidity": float(now.get("humidity", 0)),
        "wind_dir": now.get("windDir", ""),
        "wind_scale": now.get("windScale", ""),
        "wind_speed": float(now.get("windSpeed", 0)),
        "aqi": a.get("data", {}).get("aqi", 0) if a.get("status") == "ok" else 0
    }
