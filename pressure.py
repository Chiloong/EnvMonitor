import time
import requests
from config import *

def get_pressure():
    data = requests.get(OPENWEATHER_URL, params={
        "lat": LAT, "lon": LON, "appid": API_KEY, "units": "metric"
    }, timeout=10).json()
    return data["main"]["pressure"]

def read_last():
    try:
        p, t = open(PRESSURE_FILE).read().split(",")
        return float(p), float(t)
    except:
        return None

def save(p, t):
    open(PRESSURE_FILE, "w").write(f"{p},{t}")

def get_pressure_signals():
    now = time.time()
    p = get_pressure()
    low = p < 1000  # ✅ 阈值更新为1000 hPa
    rate_trigger = False

    last = read_last()
    if last:
        lp, lt = last
        dt = (now - lt)/3600
        if dt > 0:
            rate = (p - lp)/dt
            if abs(rate) > PRESSURE_RATE_THRESHOLD:
                rate_trigger = True

    save(p, now)
    return low, rate_trigger, p
