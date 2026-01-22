import os
import requests

def send_message(text: str):
    bot_token = os.getenv("8274044643:AAFd4_sK0zqhw6PMj3K3VwSSDwEx5fhffPQ", "")
    chat_id = os.getenv("7239938442", "")

    if not bot_token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass