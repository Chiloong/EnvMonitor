from config import *

def detect(data, prev):
    events = []

    # 🌬️风
    if data["wind_dir"] == "东北风":
        events.append("wind_ne")

    # 🌨️气压
    if data["pressure"] < PRESSURE_LOW:
        events.append("pressure_low")

    # 📉ΔP
    if prev:
        dp = abs(data["pressure"] - prev["pressure"])
        if dp < DP_WEAK:
            dp_level = "🟢弱波动"
        elif dp < DP_STRONG:
            dp_level = "🟡中波动"
        else:
            dp_level = "🔴强波动"
    else:
        dp_level = "🟢弱波动"

    # 😷AQI
    if data["aqi"] > AQI_HIGH:
        events.append("aqi_high")

    # 🌫️湿度
    if data["humidity"] > HUMIDITY_HIGH:
        events.append("humidity_high")

    return events, dp_level
