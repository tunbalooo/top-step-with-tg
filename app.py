import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

def send_telegram_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        return {"ok": False, "error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}

    r = requests.post(url, json=payload, timeout=10)
    return {"ok": r.ok, "status": r.status_code, "text": r.text[:200]}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    symbol    = data.get("symbol", "N/A")
    direction = str(data.get("direction", "N/A")).upper()
    price     = data.get("price", "N/A")
    timeframe = data.get("timeframe", "N/A")
    setup     = data.get("setup", "N/A")

    sl    = data.get("sl", "N/A")
    tp    = data.get("tp", "N/A")
    grade = data.get("grade", "N/A")
    score = data.get("score", "N/A")

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

    result = send_telegram_message(msg)
    return jsonify(result), (200 if result.get("ok") else 500)

@app.route("/test-telegram")
def test():
    result = send_telegram_message("✅ Telegram test from Railway is working.")
    return jsonify(result), (200 if result.get("ok") else 500)

@app.route("/")
def home():
    return "Bot running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
