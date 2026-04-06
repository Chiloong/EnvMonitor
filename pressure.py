import requests
import os
import time

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]

STATE_FILE = "state/pressure.txt"


def send_bark(msg):
    requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip().split(",")
    except:
        return None


def save_state(p, t, level):
    os.makedirs("state", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(f"{p},{t},{level}")


def get_pressure():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    data = requests.get(url, timeout=10).json()
    return data["main"]["pressure"]


def get_level(rate):
    r = abs(rate)
    if r < 0.5:
        return "STABLE"
    elif r < 1.5:
        return "MILD"
    elif r < 3:
        return "MEDIUM"
    else:
        return "STRONG"


def check_pressure():
    try:
        current_p = get_pressure()
        current_t = time.time()

        last = load_state()

        # 第一次运行
        if not last:
            save_state(current_p, current_t, "INIT")
            return

        last_p, last_t, last_level = last
        last_p = float(last_p)
        last_t = float(last_t)

        delta_p = current_p - last_p
        delta_t = (current_t - last_t) / 3600  # 小时

        if delta_t == 0:
            return

        rate = delta_p / delta_t
        level = get_level(rate)

        print(f"气压:{current_p}hPa 速率:{rate:.2f}hPa/h 等级:{level}")

        # 状态变化才提醒
        if True:
            direction = "📉下降" if rate < 0 else "📈上升"

            send_bark(
                f"🌡气压异常 {direction}\n"
                f"速率:{rate:.2f} hPa/h\n"
                f"等级:{level}"
            )

        save_state(current_p, current_t, level)

    except Exception as e:
        print("Pressure Error:", e)
