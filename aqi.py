import requests
from config import *

def get_aqi():
    try:
        url = WAQI_URL.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        data = requests.get(url, timeout=10).json()

        if data.get("status") != "ok":
            print("❌ AQI接口异常")
            return False, 0

        aqi = data["data"]["aqi"]

        trigger = aqi >= AQI_THRESHOLD

        print(f"🟥 AQI:{aqi} 触发:{trigger}")

        return trigger, aqi

    except Exception as e:
        print("❌ AQI Error:", e)
        return False, 0
