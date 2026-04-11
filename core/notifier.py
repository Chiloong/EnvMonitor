import requests
from config import BARK_KEY


def send(msg):
    print("bark send")

    try:
        lines = msg.split("\n")

        title = lines[0]
        body = "\n".join(lines[1:])

        url = f"https://api.day.app/push"

        data = {
            "device_key": BARK_KEY,
            "title": title,
            "body": body
        }

        r = requests.post(url, json=data, timeout=10)
        print(r.status_code, r.text)

    except Exception as e:
        print("bark error", e)
