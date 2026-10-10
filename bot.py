import os
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=20
    )


@app.route("/", methods=["GET"])
def home():
    return "UOFG46 Medical Exam Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True)

    if not update:
        return "OK"

    message = update.get("message")

    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(
                chat_id,
                "🧠 مرحباً بك في UOFG46 Medical Exam Bot!\n\n"
                "🦠 Bacteriology\n"
                "🍄 Mycology\n"
                "🧬 Immunology\n"
                "🔬 Pathology\n\n"
                "🚀 نظام الامتحان سيتم تجهيزه قريباً."
            )

        elif text == "/help":
            send_message(
                chat_id,
                "📚 أوامر البوت:\n\n"
                "/start - بدء البوت\n"
                "/help - المساعدة"
            )

        else:
            send_message(
                chat_id,
                "استخدم /start لبدء البوت 🚀"
            )

    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
