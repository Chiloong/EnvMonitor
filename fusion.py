import requests
import os

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]


def send_bark(msg):
    try:
        url = f"https://api.day.app/{BARK_KEY}/{msg}"
        print("🚀 联动推送:", msg)
        requests.get(url, timeout=10)
    except Exception as e:
        print("❌ Bark错误:", e)


def get_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    data = requests.get(url, timeout=10).json()
    return data


def check_fusion():
    print("🧠 联动模块运行")

    try:
        data = get_weather()

        wind = data.get("wind", {})
        pressure = data.get("main", {}).get("pressure", 0)

        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", -1)

        # 👉 东北风判断（复用你原逻辑）
        is_ne = 20 <= wind_deg <= 100
        strong_wind = wind_speed >= 2.5

        # 👉 简化气压趋势判断（当前 vs 标准）
        low_pressure = pressure < 1005  # 可调

        print(f"🌬 风速:{wind_speed} | 风向:{wind_deg}")
        print(f"🌡 气压:{pressure}")

        # 🚨 联动核心逻辑
        if is_ne and strong_wind and low_pressure:
            msg = (
                f"🚨高风险环境\n"
                f"东北风 + 低气压\n"
                f"风速:{wind_speed}m/s\n"
                f"气压:{pressure}hPa\n\n"
                f"建议:\n"
                f"- 关闭新风\n"
                f"- 降低交易频率\n"
                f"- 注意状态波动"
            )
            send_bark(msg)

    except Exception as e:
        print("❌ Fusion Error:", e)
