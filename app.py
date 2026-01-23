import os
import threading
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

def _send_telegram(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID", flush=True)
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}

    try:
        r = requests.post(url, json=payload, timeout=(2, 3))
        print("Telegram:", r.status_code, r.text[:120], flush=True)
    except Exception as e:
        print("Telegram error:", str(e), flush=True)

def send_telegram_async(text: str):
    threading.Thread(target=_send_telegram, args=(text,), daemon=True).start()

@app.get("/ping")
def ping():
    return "pong", 200

@app.get("/test-telegram")
def test_telegram():
    send_telegram_async("✅ Telegram test from Railway is working.")
    return jsonify({"ok": True}), 200

@app.post("/webhook")
def webhook():
    data = request.get_json(silent=True) or {}
    print("TV WEBHOOK:", data, flush=True)

    symbol    = data.get("symbol", "N/A")
    direction = str(data.get("direction", "N/A")).upper()
    price     = data.get("price", "N/A")
    timeframe = data.get("timeframe", "N/A")
    setup     = data.get("setup", "N/A")

    sl    = data.get("sl", "N/A")
    tp    = data.get("tp", "N/A")
    grade = data.get("grade", "N/A")
    score = data.get("score", "N/A")
    notes = data.get("notes", "")

    strategy = data.get("strategy", "")  # "APPROVED" for short format

    # Short APPROVED format
    if strategy == "APPROVED":
        msg = (
            f"✅ *APPROVED* — *{symbol}* *{direction}*\n"
            f"Setup: `{setup}`\n"
            f"Score: *{score}*\n"
            f"Entry: `{price}`"
        )

    # Full SL/TP format
    else:
        msg = (
            f"📊 *TRADE ALERT*\n\n"
            f"*{symbol}* — *{direction}*\n"
            f"Setup: `{setup}`\n"
            f"TF: `{timeframe}`\n\n"
            f"Entry: `{price}`\n"
            f"SL: `{sl}`\n"
            f"TP: `{tp}`\n"
            f"Grade: *{grade}*  Score: *{score}*"
        )
        if notes:
            msg += f"\n\nNotes: _{notes}_"

    # Don’t block requests
    send_telegram_async(msg)
    return jsonify({"ok": True}), 200

@app.get("/")
def home():
    return "Bot running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
