import requests
import os
import time

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]

STATE_FILE = "pressure_state.txt"


def send_bark(msg):
    requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)


def get_pressure():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    data = requests.get(url, timeout=10).json()
    return data["main"]["pressure"]


def read_last():
    try:
        with open(STATE_FILE, "r") as f:
            p, t = f.read().split(",")
            return float(p), float(t)
    except:
        return None


def save_current(p, t):
    with open(STATE_FILE, "w") as f:
        f.write(f"{p},{t}")


def check_pressure():
    try:
        current_p = get_pressure()
        current_t = time.time()

        last = read_last()

        if last:
            last_p, last_t = last
            delta_p = current_p - last_p
            delta_t = (current_t - last_t) / 3600

            if delta_t > 0:
                rate = delta_p / delta_t
                print(f"速率: {rate:.2f} hPa/h")

                if abs(rate) > 1.0:
                    send_bark(f"🌡气压变化异常 {rate:.2f} hPa/h")

        save_current(current_p, current_t)

    except Exception as e:
        print("Pressure Error:", e)
