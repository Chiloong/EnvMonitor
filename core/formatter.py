def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"


# =========================
# 🔥统一事件映射
# =========================
def build_event_text(events):

    event_map = {
        "wind_ne": ("💨东北风", 1),
        "aqi_high": ("🌫️高污染", 2),
        "pressure_change": ("〽️气压变", 3),
        "pressure_low": ("🌨️气压低", 4),
        "humidity_high": ("🫧高湿度", 5),
    }

    items = []

    for e in events:
        if e in event_map:
            items.append(event_map[e])

    items.sort(key=lambda x: x[1])

    # 👉 强制拼接（不允许空）
    return "".join([i[0] for i in items])


# =========================
# 🔥主输出（统一入口）
# =========================
def format_event(events, data, dp_level, risk):

    color = get_risk_color(risk)

    event_text = build_event_text(events)

    # ===== 等级 =====
    level = ""

    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"
    else:
        level = "🟢单项气象预警"

    # =========================
    # 🔥统一输出结构（关键修复点）
    # =========================
    return "\n".join([
        level,
        f"📉{dp_level}",
        f"🧠风险{color}{risk}/100",
        f"🌏环境异常组合：{event_text}"
    ])


def format_heartbeat(data, dp_level, risk):

    color = get_risk_color(risk)

    return (
        "🌏EnvAlert☀️天气恢复正常✅\n"
        f"气压{data['pressure']} 湿度{data['humidity']}% 风{data['wind_dir']} AQI{data['aqi']}\n"
        f"📉{dp_level} 🧠风险{color}{risk}/100"
    )
