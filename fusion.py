import os
import requests
import time
from config import *
from wind import get_wind
from pressure import get_pressure_signals
from aqi import get_aqi_signals

def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def read_state():
    try:
        return int(open(STATE_FILE).read().strip())
    except:
        return 0

def save_state(v):
    open(STATE_FILE, "w").write(str(v))

def check_all():

    wind_t = get_wind()
    low_t, pressure_drop = get_pressure_signals()
    aqi_high, aqi_rise, aqi = get_aqi_signals()

    last = read_state()

    # ======================
    # 🧠 真实风险（不变）
    # ======================
    real_count = sum([wind_t, low_t, pressure_drop, aqi_high])

    # ======================
    # 🟡 趋势信号（新增）
    # ======================
    trend_flag = 1 if (aqi_rise or (pressure_drop and wind_t)) else 0

    msg = None

    # ======================
    # 🟡 趋势预警（只触发一次）
    # ======================
    if trend_flag == 1 and last == 0:
        if aqi_rise:
            msg = f"⚠️AQI快速上升📈 当前{aqi}"
        elif pressure_drop and wind_t:
            msg = "⚠️气压下降+东北风🌬"

    # ======================
    # 🔴 原有报警逻辑（完全保留）
    # ======================
    elif real_count > last:

        if real_count == 1:
            if wind_t:
                msg = "🚨EnvAlert🚨\n🏭发电厂↙️东北风💨触发\n⛔️关闭新风🟣颗粒过滤开大⬆️"
            elif low_t:
                msg = f"🚨EnvAlert🚨\n✴️气压🌨️过低🥱 当前气压:{get_pressure_signals()[2]} hPa"
            elif aqi_high:
                msg = f"🚨EnvAlert🚨\n🟥高污染AQI{aqi}+😷"

        elif real_count == 2:
            msg = "1️⃣🟡气象预警🚨"
        elif real_count == 3:
            msg = "2️⃣🟠气象预警🚨"
        elif real_count >= 4:
            msg = "3️⃣🔴气象预警🚨"

    # ======================
    # 🟢 恢复逻辑（保留）
    # ======================
    elif real_count < last:
        if real_count == 0:
            msg = "🟢EnvAlert恢复正常"
        elif last >= 2 and real_count == 1:
            msg = "🟢气象风险下降"

    # 🔹 调试输出
    print(f"🔹 调试输出信号状态:")
    print(f"风速/风向/阵风触发: {wind_t}")
    print(f"气压低: {low_t}  气压下降速率触发: {pressure_drop}")
    print(f"AQI高污染: {aqi_high}  AQI快速上升: {aqi_rise}  当前AQI: {aqi}")
    print(f"当前真实计数: {real_count} 上次: {last}")

    if msg:
        send(msg)

    # ⚠️ 只记录真实状态（关键）
    save_state(real_count)

    print(f"当前:{real_count} 上次:{last}")
