import requests
import time
from config import *

def get_pressure():
    """从 OpenWeather 获取实时气压"""
    try:
        data = requests.get(OPENWEATHER_URL, params={
            "lat": LAT,
            "lon": LON,
            "appid": API_KEY,
            "units": "metric"
        }, timeout=10).json()
        return data["main"]["pressure"]
    except Exception as e:
        print(f"❌ 获取气压异常: {e}")
        return None

def read_last():
    """读取上一次气压值及时间"""
    try:
        p, t = open(PRESSURE_FILE).read().split(",")
        return float(p), float(t)
    except:
        return None

def save(p, t):
    """保存当前气压值及时间"""
    open(PRESSURE_FILE, "w").write(f"{p},{t}")

def get_pressure_signals():
    """
    返回：
        low: 是否低于阈值
        rate_trigger: 气压下降/上升速率是否超过阈值
        current_pressure: 当前气压值（用于提醒显示）
    """
    now = time.time()
    p = get_pressure()
    if p is None:
        return False, False, None

    # 🔹 调试输出当前气压
    print(f"📊 当前气压: {p} hPa  阈值: {PRESSURE_LOW} hPa")

    low = p < PRESSURE_LOW
    rate_trigger = False

    last = read_last()
    if last:
        lp, lt = last
        dt = (now - lt) / 3600  # 转小时
        if dt > 0:
            rate = (p - lp) / dt
            if abs(rate) > PRESSURE_RATE_THRESHOLD:
                rate_trigger = True

    save(p, now)
    return low, rate_trigger, p
