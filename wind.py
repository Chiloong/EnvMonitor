import requests
from config import *

def get_wind():
    try:
        data = requests.get(
            OPENWEATHER_URL,
            params={
                "lat": LAT,
                "lon": LON,
                "appid": API_KEY,
                "units": "metric"
            },
            timeout=10
        ).json()

        wind = data.get("wind", {})
        speed = wind.get("speed", 0)
        deg = wind.get("deg", -1)
        gust = wind.get("gust", 0)

        trigger = (
            (speed >= WIND_SPEED_THRESHOLD or gust >= GUST_THRESHOLD)
            and (NE_MIN <= deg <= NE_MAX)
        )

        print(f"🌬 风速:{speed} 风向:{deg} 阵风:{gust} 触发:{trigger}")

        return trigger

    except Exception as e:
        print("❌ Wind Error:", e)
        return False
