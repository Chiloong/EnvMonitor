from config import *


def detect(data, prev):
    events = []

    # 🌬️东北风判断（用角度）
    angle = data.get("wind_angle", 0)

    # 东北风范围：20° ~ 100°
    if 20 <= angle <= 100:
        events.append("wind_ne")

    # 🌨️气压
    if data["pressure"] < PRESSURE_LOW:
        events.append("pressure_low")

    # 😷AQI
    if data["aqi"] > AQI_HIGH:
        events.append("aqi_high")

    # 🌫️湿度
    if data["humidity"] > HUMIDITY_HIGH:
        events.append("humidity_high")

    # 📉ΔP变化率
    if prev:
        dp = abs(data["pressure"] - prev["pressure"])
        if dp < DP_WEAK:
            dp_level = "🟢弱"
        elif dp < DP_STRONG:
            dp_level = "🟡中"
        else:
            dp_level = "🔴强"
    else:
        dp_level = "🟢弱"

    return events, dp_level
