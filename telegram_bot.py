import os
import requests

def send_message(text: str):
    bot_token = os.getenv("8274044643:AAFd4_sK0zqhw6PMj3K3VwSSDwEx5fhffPQ", "")
    chat_id = os.getenv("7239938442", "")

    if not bot_token or not chat_id:
        return {"ok": False, "error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        r = requests.post(url, json=payload, timeout=10)
        return {"ok": r.ok, "status_code": r.status_code, "text": r.text[:300]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
