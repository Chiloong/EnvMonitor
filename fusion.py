import time
import requests
import json
from config import *
from wind import get_wind
from pressure import get_pressure_signals
from aqi import get_aqi_signals

# ======================
# 🔔 推送
# ======================
def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

# ======================
# 📁 状态（总）
# ======================
def read_state():
    try:
        return int(open(STATE_FILE).read().strip())
    except:
        return 0

def save_state(v):
    open(STATE_FILE, "w").write(str(v))

# ======================
# 🟢 恢复节流
# ======================
def read_recovery_time():
    try:
        return float(open(RECOVERY_FILE).read().strip())
    except:
        return 0

def save_recovery_time(t):
    open(RECOVERY_FILE, "w").write(str(t))

# ======================
# 🧠 信号级状态机
# ======================
def read_signal_state():
    try:
        return json.loads(open(SIGNAL_STATE_FILE).read())
    except:
        return {
            "aqi_high": False,
            "pressure_low": False,
            "wind": False,
            "humidity": False
        }

def save_signal_state(s):
    open(SIGNAL_STATE_FILE, "w").write(json.dumps(s))

# ======================
# ⏱ 动态频率（新增）
# ======================
def should_run(risk):
    now = time.time()
    hour = time.localtime(now).tm_hour

    try:
        last = float(open("run_state.txt").read())
    except:
        last = 0

    is_night = (hour >= 23 or hour < 7)

    if risk:
        interval = 300
    elif is_night:
        interval = 1800
    else:
        interval = 900

    if now - last < interval:
        print(f"⏭ 跳过 | 间隔:{interval}s")
        return False

    open("run_state.txt", "w").write(str(now))
    return True

# ======================
# 🌫 湿度（新增）
# ======================
def get_humidity():
    try:
        import requests
        res = requests.get(OPENWEATHER_URL, params={
            "lat": LAT,
            "lon": LON,
            "appid": API_KEY,
            "units": "metric"
        }, timeout=10).json()
        return res["main"]["humidity"]
    except:
        return 0

# ======================
# 🚀 主逻辑
# ======================
def check_all():

    wind_t = get_wind()
    low_t, pressure_drop, current_pressure = get_pressure_signals()
    aqi_high, aqi_rise, aqi = get_aqi_signals()
    humidity = get_humidity()
    humidity_t = humidity > 60

    last_total = read_state()
    last_signals = read_signal_state()

    current_signals = {
        "aqi_high": aqi_high,
        "pressure_low": low_t,
        "wind": wind_t,
        "humidity": humidity_t
    }

    real_count = sum(current_signals.values())

    # ⏱ 动态频率控制
    if not should_run(real_count > 0):
        return

    msg = None
    now = time.time()

    # ======================
    # 🔴 单项触发
    # ======================
    if not last_signals["humidity"] and humidity_t:
        msg = "🚨EnvAlert🚨\n✴️湿度🫧过高😶‍🌫️\n⛔️关闭新风▶️开除湿机"

    elif not last_signals["aqi_high"] and aqi_high:
        msg = f"🚨高污染 AQI:{aqi}"

    elif not last_signals["pressure_low"] and low_t:
        msg = f"🚨气压过低 当前:{current_pressure}hPa"

    elif not last_signals["wind"] and wind_t:
        msg = "🚨东北风触发 关闭新风"

    # ======================
    # 🟢 单项恢复
    # ======================
    elif last_signals["humidity"] and not humidity_t:
        msg = f"🟢湿度恢复 当前:{humidity}%"

    elif last_signals["aqi_high"] and not aqi_high:
        msg = f"🟢AQI恢复正常 当前:{aqi}"

    elif last_signals["pressure_low"] and not low_t:
        msg = f"🟢气压恢复 当前:{current_pressure}hPa"

    elif last_signals["wind"] and not wind_t:
        msg = "🟢风向恢复"

    # ======================
    # 🟡 组合预警（新增）
    # ======================
    if real_count == 2:
        msg = "🟡1️⃣级气象预警🚨"
    elif real_count == 3:
        msg = "🟠2️⃣级气象预警🚨"
    elif real_count >= 4:
        msg = "🔴3️⃣级气象预警🚨"

    # ======================
    # 🟢 全局恢复（12小时）
    # ======================
    elif last_total > 0 and real_count == 0:
        last_time = read_recovery_time()
        if now - last_time > 12 * 3600:
            msg = "🟢EnvAlert恢复正常"
            save_recovery_time(now)

    # ======================
    # ⚠️ 趋势（保留）
    # ======================
    elif aqi_rise:
        msg = f"⚠️AQI快速上升 当前:{aqi}"

    elif pressure_drop and wind_t:
        msg = "⚠️气压下降+东北风"

    # ======================
    # 📤 推送
    # ======================
    if msg:
        send(msg)

    save_state(real_count)
    save_signal_state(current_signals)

    # ======================
    # 🔍 调试
    # ======================
    print("------状态机------")
    print("当前:", current_signals)
    print(f"湿度:{humidity} 触发:{humidity_t}")
    print(f"风险数:{real_count}")
