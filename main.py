print("=== RUNNING ===")

from core.sensor import fetch_all
from core.engine import detect
from core.state import can_trigger, heartbeat_due
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
        log("ERROR empty data")
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

    # =========================
    # 🌙心跳
    # =========================
    if heartbeat_due(HEARTBEAT_INTERVAL):
        msg = format_heartbeat(data, dp_level, risk)
        log("heartbeat")
        send(msg)

    # =====================================================
    # 🔥1️⃣ 单事件推送（恢复）
    # =====================================================
    for e in events:

        key = "single:" + e

        if can_trigger(key):

            msg = format_event([e], data, dp_level, risk)

            log(f"single_event={e}")

            send(msg)

    # =====================================================
    # 🔥2️⃣ 组合事件推送（保留）
    # =====================================================
    if len(events) >= 2:

        combo_key = "combo:" + ",".join(sorted(events))

        if can_trigger(combo_key):

            msg = format_event(events, data, dp_level, risk)

            log(f"combo_event={events}")

            send(msg)


if __name__ == "__main__":
    main()
