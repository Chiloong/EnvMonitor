def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"


def format_event(events, data, dp_level, risk):

    color = get_risk_color(risk)

    # 🔴多事件等级
    level = ""

    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"

    lines = ["🚨EnvAlert🚨"]

    if "wind_ne" in events:
        lines.append(f"🏭发电厂↙️东北风{data['wind_scale']}级💨")

    if "pressure_low" in events:
        lines.append(f"✴️气压🌨️过低🥱{data['pressure']}hPa")

    if "aqi_high" in events:
        lines.append(f"🟥高污染🌫️AQI{data['aqi']}😷")

    if "humidity_high" in events:
        lines.append(f"✴️湿度🫧过高😶‍🌫️{data['humidity']}%")

    # 📉ΔP + 风险（颜色版）
    lines.append(f"📉ΔP:{dp_level} 🧠风险{color}{risk}/100")

    # 🔴多事件覆盖
    if level:
        return "\n".join([
            level,
            f"📉{dp_level}",
            f"🧠风险{color}{risk}/100",
            f"🌏环境异常组合"
        ])

    return "\n".join(lines[:4])


def format_heartbeat(data, dp_level, risk):

    color = get_risk_color(risk)

    return (
        "🌏EnvAlert☀️天气恢复正常✅\n"
        f"气压{data['pressure']} 湿度{data['humidity']}% 风{data['wind_dir']} AQI{data['aqi']}\n"
        f"📉{dp_level} 🧠风险{color}{risk}/100"
    )
