from config import *


def detect(data, prev):

    events = []

    angle = data.get("wind_angle", 0)

    # 🌬️东北风
    if 20 <= angle <= 100:
        events.append("wind_ne")

    # 🌨️气压低
    if data["pressure"] < PRESSURE_LOW:
        events.append("pressure_low")

    # 🌫️AQI高
    if data["aqi"] > AQI_HIGH:
        events.append("aqi_high")

    # 🫧湿度高
    if data["humidity"] > HUMIDITY_HIGH:
        events.append("humidity_high")

    # 〽️气压变化
    pressure_change = False
    if prev:
        dp = abs(data["pressure"] - prev["pressure"])
        if dp > DP_WEAK:
            pressure_change = True

    if pressure_change:
        events.append("pressure_change")

    # =========================
    # 🧠风险评分
    # =========================
    risk = 0

    weight = {
        "wind_ne": 20,
        "pressure_low": 30,
        "aqi_high": 30,
        "humidity_high": 20,
        "pressure_change": 10
    }

    for e in events:
        risk += weight.get(e, 10)

    risk = min(risk, 100)

    # =========================
    # 📉ΔP等级
    # =========================
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

    return events, dp_level, risk
