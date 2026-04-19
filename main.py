import telebot
import smtplib
import random
import time
from email.mime.text import MIMEText
from telebot import types
from flask import Flask
from threading import Thread

# --- АНТИ-СОН ---
app = Flask('')
@app.route('/')
def home(): return "System Online"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- КОНФИГ ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
MY_EMAIL = 'p.st.v@mail.ru'
MY_APP_PASSWORD = 'itmsluvppzoxbtyi'

bot = telebot.TeleBot(TOKEN)

# Данные для жалоб из твоих файлов
RECIPIENTS = ['abuse@telegram.org', 'support@telegram.org']
REPORTS = [
    "Hello, I report user {target} for distributing illegal content.",
    "This account {target} is violating Telegram ToS (Scam/Doxing).",
    "Please check {target} for prohibited materials and spam attack."
]

# --- КНОПКИ ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💀 МАССОВЫЙ СНОС", "🔍 ПРОБИВ (OSINT)")
    markup.add("📂 МАНУАЛЫ", "🛡 АНОНИМНОСТЬ")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🛰 **GALAXY V14.0 READY**\n\nВсе системы из твоих .py файлов активны. Использую почту: " + MY_EMAIL, reply_markup=main_menu(), parse_mode='Markdown')

# --- ЛОГИКА КНОПОК ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "💀 МАССОВЫЙ СНОС":
        bot.send_message(message.chat.id, "🎯 **Введи @username или ссылку на цель:**")
        bot.register_next_step_handler(message, run_snos)
    
    elif message.text == "🔍 ПРОБИВ (OSINT)":
        bot.send_message(message.chat.id, "🎯 **Введи НОМЕР (+7...) или НИК:**")
        bot.register_next_step_handler(message, run_osint)
        
    elif message.text == "📂 МАНУАЛЫ":
        bot.send_message(message.chat.id, "📚 **МАНУАЛЫ (Из твоих баз):**\n1. Снос через почту (Active)\n2. Пробив через логи (Pending)")

# --- ФУНКЦИЯ СНОСА ---
def run_snos(message):
    target = message.text
    bot.send_message(message.chat.id, f"🚀 **АТАКА НАЧАТА!**\nЦель: {target}\nОтправляю пачку жалоб...")
    
    try:
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(MY_EMAIL, MY_APP_PASSWORD)
        
        success = 0
        for i in range(5): # 5 циклов по 2 почты = 10 репортов за раз
            for rec in RECIPIENTS:
                msg = MIMEText(random.choice(REPORTS).format(target=target))
                msg['Subject'] = "Abuse Report"
                msg['From'] = MY_EMAIL
                msg['To'] = rec
                server.send_message(msg)
                success += 1
            time.sleep(1)
        
        server.quit()
        bot.send_message(message.chat.id, f"✅ **ГОТОВО!** Отправлено {success} жалоб.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка почты: {e}")

# --- ФУНКЦИЯ ОСИНТА ---
def run_osint(message):
    val = message.text
    if val.startswith('+'):
        phone_clean = val.replace('+', '')
        res = (
            f"📱 **РЕЗУЛЬТАТ ПО НОМЕРУ:** `{val}`\n\n"
            f"🔗 [Открыть в WhatsApp](https://wa.me/{phone_clean})\n"
            f"🔗 [Поиск в TrueCaller](https://www.truecaller.com/search/ru/{val})\n"
            f"🔗 [Проверить в Telegram](tg://resolve?phone={phone_clean})\n"
            f"🔗 [Глаз Бога (Поиск)](https://t.me/EyeGods_Bot)"
        )
    else:
        res = (
            f"👤 **НИК:** `{val}`\n\n"
            f"🔗 [Поиск в VK](https://vk.com/search?c%5Bq%5D={val})\n"
            f"🔗 [Поиск в Google](https://www.google.com/search?q=%22{val}%22)\n"
            f"🔗 [Sherlock Check](https://google.com/search?q=site:instagram.com+{val})"
        )
    bot.send_message(message.chat.id, res, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
