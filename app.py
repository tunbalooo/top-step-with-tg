import os
from flask import Flask, request, jsonify
from telegram_bot import send_message

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Prop Coach is running"

@app.route("/test-telegram", methods=["GET"])
def test_telegram():
    result = send_message("✅ Telegram test from Railway is working.")
    return jsonify(result)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}

    print("WEBHOOK HIT:", data, flush=True)

    symbol = data.get("symbol", "NQ")
    direction = str(data.get("direction", "")).upper()
    price = data.get("price", "")
    setup = data.get("setup", "UNKNOWN")
    notes = str(data.get("notes", ""))

    score = 65
    if "sweep" in notes.lower(): score += 10
    if "reclaim" in notes.lower(): score += 10
    if "strong" in notes.lower(): score += 5

    if direction in ["BUY", "SELL"]:
        msg = f"✅ APPROVED — {symbol} {direction}\nSetup: {setup}\nScore: {score}\nEntry: {price}"
    else:
        msg = f"❌ REJECTED — {symbol}\nReason: invalid direction\nRaw: {data}"

    result = send_message(msg)
    print("TELEGRAM RESULT:", result, flush=True)

    return jsonify({"received": data, "telegram": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
