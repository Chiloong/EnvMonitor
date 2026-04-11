import requests
from config import BARK_KEY

def send(msg):
    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    requests.get(url, timeout=10)
