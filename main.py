from flask import Flask, request
import requests
import json

app = Flask(__name__)

with open("config.json") as f:
    config = json.load(f)

TELEGRAM_TOKEN = config["bot_token"]
TELEGRAM_CHAT_ID = config["chat_id"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "Bot is alive!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        message = data.get("message", "No 'message' field received.")
        send_telegram_message(f"📈 *TradingView сигнал:*
{message}")
        return "Message sent!", 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run()
