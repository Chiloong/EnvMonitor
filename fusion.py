import time
import requests
import json
from config import *

# ======================
# 🔔 推送
# ======================
def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

# ======================
# 📡 获取数据（单次API）
# ======================
def fetch_all():
    weather = requests.get(
        f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}",
        timeout=10
    ).json()

    aqi_data = requests.get(
        WAQI_URL.format(lat=LAT, lon=LON, token=WAQI_TOKEN),
        timeout=10
    ).json()

    now = weather["now"]

    return {
        "pressure": float(now["pressure"]),
        "humidity": float(now["humidity"]),
        "wind_speed": float(now["windSpeed"]),
        "wind_dir": float(now["wind360"]),
        "aqi": int(aqi_data["data"]["aqi"])
    }

# ======================
# 📁 状态读写
# ======================
def read_json(file, default):
    try:
        return json.loads(open(file).read())
    except:
        return default

def save_json(file, data):
    open(file, "w").write(json.dumps(data))

# ======================
# 📊 历史数据（12小时）
# ======================
def update_history(data):
    history = read_json(HISTORY_FILE, [])

    now = time.time()
    history.append({"t": now, **data})

    # 保留12小时
    history = [i for i in history if now - i["t"] < 12 * 3600]

    save_json(HISTORY_FILE, history)
    return history

def analyze_history(history):
    if not history:
        return None

    min_pressure = min(i["pressure"] for i in history)
    max_aqi = max(i["aqi"] for i in history)

    return min_pressure, max_aqi

# ======================
# 🚀 主逻辑
# ======================
def check_all():

    data = fetch_all()

    pressure = data["pressure"]
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]
    wind_dir = data["wind_dir"]
    aqi = data["aqi"]

    # ======================
    # 信号判断
    # ======================
    wind_t = wind_speed > WIND_SPEED_THRESHOLD and 20 < wind_dir < 100
    pressure_low = pressure < PRESSURE_LOW
    humidity_high = humidity > HUMIDITY_THRESHOLD
    aqi_high = aqi > AQI_THRESHOLD

    signals = {
        "wind": wind_t,
        "pressure": pressure_low,
        "humidity": humidity_high,
        "aqi": aqi_high
    }

    count = sum(signals.values())

    # ======================
    # 趋势（简单版）
    # ======================
    history = update_history(data)
    summary = analyze_history(history)

    pressure_drop = False
    aqi_rise = False

    if len(history) > 2:
        pressure_drop = history[-1]["pressure"] < history[-2]["pressure"]
        aqi_rise = history[-1]["aqi"] > history[-2]["aqi"]

    # ======================
    # 状态机
    # ======================
    last_signals = read_json(SIGNAL_STATE_FILE, signals)
    last_total = int(open(STATE_FILE).read()) if os.path.exists(STATE_FILE) else 0

    msg = None
    now = time.time()

    # 🚨 单项触发
    if not last_signals.get("humidity") and humidity_high:
        msg = "🚨EnvAlert🚨\n✴️湿度🫧过高😶‍🌫️\n⛔️关闭新风▶️开除湿机"

    elif not last_signals.get("pressure") and pressure_low:
        msg = f"🚨气压过低 当前:{pressure}"

    elif not last_signals.get("aqi") and aqi_high:
        msg = f"🚨高污染 AQI:{aqi}"

    elif not last_signals.get("wind") and wind_t:
        msg = "🚨东北风触发"

    # 🟡组合预警
    elif count >= 2 and last_total < 2:
        if count == 2:
            msg = "🟡1️⃣级气象预警🚨"
        elif count == 3:
            msg = "🟠2️⃣级气象预警🚨"
        elif count >= 4:
            msg = "🔴3️⃣级气象预警🚨"

    # 🟢恢复 + 完整播报
    elif last_total > 0 and count == 0:
        last_time = read_json(RECOVERY_FILE, 0)

        if now - last_time > 12 * 3600:

            min_p, max_aqi = summary if summary else (pressure, aqi)

            msg = f"""🟢EnvAlert恢复正常

📊当前状态：
🌡气压: {pressure} hPa
💧湿度: {humidity}%
🌫AQI: {aqi}
🌬风: 正常

📈趋势：
AQI变化: {"上升" if aqi_rise else "稳定"}
气压变化: {"下降" if pressure_drop else "稳定"}

📉过去12小时：
最低气压: {min_p}
AQI峰值: {max_aqi}
"""

            save_json(RECOVERY_FILE, now)

    # 📤 推送
    if msg:
        send(msg)

    # 保存状态
    save_json(SIGNAL_STATE_FILE, signals)
    open(STATE_FILE, "w").write(str(count))

    # 调试输出
    print(f"气压:{pressure} 湿度:{humidity} AQI:{aqi}")
    print(f"风险数:{count}")
