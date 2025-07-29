import os
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN", "8235944638:AAHKuOamXASwR5mG_mz0kwo01qqKpyK0Gjs")
ADMIN_ID = 7748794204
GROUP_IDS = [-4946626315, -4986896187]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Стартова команда ---
@bot.message_handler(commands=['start', 'test'])
def send_welcome(message):
    bot.reply_to(message, "Бот працює!")

# --- Обробка повідомлень у групі ---
@bot.message_handler(func=lambda m: m.chat.id in GROUP_IDS)
def forward_to_admin(message):
    # Переслати адміну у приват
    text = f"Від {message.from_user.first_name}:\n{message.text}"
    bot.send_message(ADMIN_ID, text)

    # Відповідь у групі
    bot.reply_to(message, f"Ви написали: {message.text}")

    # Кнопка "Зв'язатися з адвокатом"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Подзвонити", url="tel:+380983607200"))
    markup.add(InlineKeyboardButton("Написати адвокату", url="https://t.me/your_lawyer_username"))
    bot.send_message(message.chat.id,
                     "Для прямого зв'язку з адвокатом:",
                     reply_markup=markup)

# --- Flask route, щоб Render не засинав ---
@app.route('/')
def home():
    return "Bot is running!"

import threading

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()
