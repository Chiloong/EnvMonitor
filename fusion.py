import os

# ======================
# 🌍 QWeather
# ======================
QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
QWEATHER_KEY = os.environ.get("QWEATHER_KEY")

# AQI（仍用WAQI）
WAQI_URL = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
WAQI_TOKEN = os.environ.get("WAQI_TOKEN")

# ======================
# 📍 地点
# ======================
LAT = 35.21
LON = 113.29

# ======================
# 🔔 推送
# ======================
BARK_URL = "https://api.day.app"
BARK_KEY = os.environ.get("BARK_KEY")

# ======================
# ⚖️ 阈值
# ======================
WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0

PRESSURE_LOW = 1000
PRESSURE_RATE_THRESHOLD = 1.0

AQI_THRESHOLD = 180
AQI_DELTA_THRESHOLD = 15

HUMIDITY_THRESHOLD = 60   # ✅ 新增

# ======================
# 📁 状态文件
# ======================
STATE_FILE = "fusion_state.txt"
PRESSURE_FILE = "pressure_state.txt"
AQI_STATE_FILE = "aqi_state.txt"
RECOVERY_FILE = "recovery_state.txt"
SIGNAL_STATE_FILE = "signal_state.txt"

# 🆕 12小时数据缓存
HISTORY_FILE = "history.json"
