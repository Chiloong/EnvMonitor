def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"

def map_event(e):
    mapping = {
        "wind_ne":         "💨东北风",
        "pressure_low":    "🌨️气压低",
        "aqi_high":        "🌫️高污染",
        "humidity_high":   "🫧高湿度",
        "pressure_change": "〽️气压降",
    }
    return mapping.get(e, "")

def format_event(event, data, dp_level, risk):
    if event == "wind_ne":
        return "\n".join([
            "↙️东北风{data['wind_scale']}级💨",
            f"注意⚠️发电厂🏭有害气体🌋SO₂NO₂",
            "⛔️关闭新风🟣颗粒过滤开大⬆️"
        ])
    if event == "pressure_low":
        return "\n".join([
            "🚨低气压失稳🚨",
            f"✴️气压🌨️过低🥱{data['pressure']}hPa"
        ])
    if event == "pressure_change":
        return f"✴️气压〽️骤变😣ΔP{dp_level}"
    if event == "aqi_high":
        return "\n".join([
            "🚨空气重度污染🚨",
            f"🌀开大🌪️净化器🌫️AQI{data['aqi']}😷"
        ])
    if event == "humidity_high":
        return "\n".join([
            "🚨开始憋闷🚨",
            f"✴️湿度{data['humidity']}%😶‍🌫️过高💦",
            "⛔️关闭新风▶️开除湿机"
        ])
    return ""

def format_combo(events, data, dp_level, risk):
    color = get_risk_color(risk)
    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    else:
        level = "🟡1️⃣级气象预警🚨"
    event_text = "".join(map_event(e) for e in events)
    return "\n".join([
        level,
        f"📉{dp_level}",
        f"🧠风险{color}{risk}/100",
        f"🌏异常：{event_text}"
    ])

def format_heartbeat(data, dp_level, risk):
    color = get_risk_color(risk)
    return "\n".join([
        "🌏EnvAlert 定时播报",
        f"气压:{data['pressure']} 湿度:{data['humidity']}% 风:{data['wind_dir']} AQI:{data['aqi']}",
        f"📉{dp_level} 风险:{risk}{color}"
    ])
