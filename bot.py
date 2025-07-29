from flask import Flask, request
import telegram

TOKEN = "8235944638:AAHKuOamXASwR5mG_mz0kwo01qqKpyK0Gjs"
ADMIN_ID = 7748794204  # твій ID

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    # Переслати повідомлення адміну
    bot.send_message(chat_id=ADMIN_ID, text=f"Від {chat_id}: {text}")

    # Автовідповідь у групі
    bot.send_message(chat_id=chat_id, text="Ваше питання передано адвокату.")
    return "ok"

@app.route("/")
def index():
    return "Бот працює!"

if __name__ == "__main__":
    app.run(port=5000)
