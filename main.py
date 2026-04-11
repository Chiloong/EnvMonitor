from core.sensor import fetch_all
from core.engine import detect
from core.state import (
    can_trigger_event,
    can_trigger_combo,
    heartbeat_due
)
from core.formatter import format_event, format_heartbeat
from core.notifier import send
from config import HEARTBEAT_INTERVAL
import json, os


def log(msg):
    print(f"[EnvAlert] {msg}")


def main():
    log("🚀 start")

    data = fetch_all()
    log(f"data={data}")

    if not data:
        return

    os.makedirs("storage", exist_ok=True)

    prev = None
    if os.path.exists("storage/state.json"):
        try:
            prev = json.load(open("storage/state.json"))
        except:
            prev = None

    events, dp_level, risk = detect(data, prev)
    print("events =", events)

    json.dump(data, open("storage/state.json", "w"))

    if heartbeat_due(HEARTBEAT_INTERVAL):
        send(format_heartbeat(data, dp_level, risk))

    # ===== 单事件 =====
    for e in events:
        if can_trigger_event(e):
            send(format_event([e], data, dp_level, risk))
            log(f"single_event={e}")

    # ===== 组合事件 =====
    if len(events) >= 2:
        if can_trigger_combo(events):
            send(format_event(events, data, dp_level, risk))
            log(f"combo_event={events}")
