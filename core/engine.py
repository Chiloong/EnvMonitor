from config import (
    PRESSURE_LOW, AQI_HIGH, HUMIDITY_HIGH,
    DP_WEAK, DP_STRONG
)

def detect(data, prev):
    events = []

    # 🌬️东北风（2–3级风电厂羽流影响最大）
    angle = data.get("wind_angle", 0)
    if 18 <= angle <= 78:
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

    # 〽️气压下降（只有降压才触发，升压是天气好转）
    dp = (prev["pressure"] - data["pressure"]) if prev else 0
    if dp > DP_WEAK:
        events.append("pressure_change")

    # =========================
    # 🧠风险评分（总分100）
    # =========================
    weight = {
        "wind_ne":        15,
        "pressure_low":   25,
        "aqi_high":       25,
        "humidity_high":  15,
        "pressure_change": 20,
    }
    risk = min(sum(weight.get(e, 10) for e in events), 100)

    # =========================
    # 📉ΔP等级
    # =========================
    if dp < DP_WEAK:
        dp_level = "🟢弱波动"
    elif dp < DP_STRONG:
        dp_level = "🟡中波动"
    else:
        dp_level = "🔴强波动"

    return events, dp_level, risk
