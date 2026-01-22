import os
from flask import Flask, request, jsonify
from telegram_bot import send_message

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Prop Coach is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}

    symbol = data.get("symbol", "NQ")
    direction = str(data.get("direction", "")).upper()
    price = data.get("price", "")
    setup = data.get("setup", "UNKNOWN")
    notes = str(data.get("notes", ""))

    score = 65
    if "sweep" in notes.lower():
        score += 10
    if "reclaim" in notes.lower():
        score += 10
    if "strong" in notes.lower():
        score += 5

    if direction in ["BUY", "SELL"] and score >= 65:
        msg = (
            f"✅ APPROVED — {symbol} {direction}\n"
            f"Setup: {setup}\n"
            f"Score: {score}\n\n"
            f"Entry: {price}\n"
            f"Stop: Structure / ATR (wider)\n"
            f"TP: 1.3R – 2R\n"
            f"Trail: After +0.8R → ATR"
        )
        send_message(msg)
        return jsonify({"status": "APPROVE", "score": score})
    else:
        msg = (
            f"❌ REJECTED — {symbol} {direction}\n"
            f"Reason: Low score or invalid direction\n"
            f"Score: {score}"
        )
        send_message(msg)
        return jsonify({"status": "REJECT", "score": score})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
