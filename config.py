import os

# 🌍 数据源配置
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BARK_URL = "https://api.day.app"

# 📍 地点
LAT = 35.21
LON = 113.29

# 🔑 Secrets
API_KEY = os.environ.get("API_KEY")
BARK_KEY = os.environ.get("BARK_KEY")

# ⚖️ 阈值
PRESSURE_RATE_THRESHOLD = 1.0      # hPa/h
WIND_SPEED_THRESHOLD = 2.5         # m/s
GUST_THRESHOLD = 4.0               # m/s
NE_MIN = 20                        # 东北风最小角度
NE_MAX = 100                       # 东北风最大角度

# ⚙️ 状态文件
PRESSURE_STATE_FILE = "pressure_state.txt"
WIND_STATE_FILE = "wind_state.txt"
