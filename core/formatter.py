def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"

def format_event(event, data, dp_level, risk):
    """每个事件独立格式，单独推送"""

    if event == "wind_ne":
        return "\n".join([
            "🚨EnvAlert🚨",
            f"🏭发电厂↙️东北风{data['wind_scale']}级💨触发",
            "⛔️关闭新风🟣颗粒过滤开大⬆️"
        ])

    if event == "pressure_low":
        return "\n".join([
            "🚨EnvAlert🚨",
            f"✴️气压🌨️过低🥱{data['pressure']}hPa"
        ])

    if event == "pressure_change":
        return f"✴️气压〽️骤变😣ΔP{dp_level}"

    if event == "aqi_high":
        return "\n".join([
            "🚨EnvAlert🚨",
            f"🟥高污染🌫️AQI{data['aqi']}😷"
        ])

    if event == "humidity_high":
        return "\n".join([
            "🚨EnvAlert🚨",
            f"✴️湿度{data['humidity']}%😶‍🌫️过高💦",
            "⛔️关闭新风▶️开除湿机"
        ])

    return ""

def format_heartbeat(data, dp_level, risk):
    color = get_risk_color(risk)
    return "\n".join([
        "🌏EnvAlert 定时播报",
        f"气压:{data['pressure']} 湿度:{data['humidity']}% 风:{data['wind_dir']} AQI:{data['aqi']}",
        f"📉{dp_level} 风险:{risk}{color}"
    ])
