import telebot
import smtplib
import time
import random
from email.mime.text import MIMEText
from telebot import types
from flask import Flask
from threading import Thread

# --- ЖИВУЧЕСТЬ ---
app = Flask('')
@app.route('/')
def home(): return "Machine Active"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- КОНФИГ ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
MY_EMAIL = 'p.st.v@mail.ru'
MY_APP_PASSWORD = 'itmsluvppzoxbtyi' # Твой пароль из 16 букв
bot = telebot.TeleBot(TOKEN)

# --- БАЗА ЖАЛОБ (РАНДОМ) ---
SUBJECTS = ["Report for User", "Violation Abuse", "Urgent Concern", "ToS Violation", "Illegal Content"]
MESSAGES = [
    "Hello, I found a user {target} who is distributing prohibited materials. Please check and ban.",
    "Report on {target}: this user is engaging in fraudulent activities and scamming people.",
    "This account {target} is violating Telegram safety rules by posting illegal links.",
    "I want to report {target} for harassment and spreading private information (doxxing)."
]

def main_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("💀 МАССОВЫЙ СНОС (EMAIL)", "🔍 ГЛУБОКИЙ OSINT")
    m.add("⚙️ ТЕРМИНАТОР", "🛡 АНОНИМНОСТЬ")
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🛰 **GALAXY ANNIHILATOR V12.0**\nЛогика из snos.py и by.nsvl.snos.py полностью внедрена.\n\nГотов к уничтожению целей.", reply_markup=main_menu(), parse_mode='Markdown')

# --- ЛОГИКА СНОСА ---
@bot.message_handler(func=lambda m: m.text == "💀 МАССОВЫЙ СНОС (EMAIL)")
def snos_init(message):
    bot.send_message(message.chat.id, "🎯 **Введи цель (ссылка или @username):**")
    bot.register_next_step_handler(message, snos_attack)

def snos_attack(message):
    target = message.text
    bot.send_message(message.chat.id, f"🚀 **АТАКА ЗАПУЩЕНА!**\nЦель: {target}\nИспользую твою почту для обхода фильтров...")
    
    success = 0
    try:
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(MY_EMAIL, MY_APP_PASSWORD)
        
        # Цикл как в твоих .py файлах (сделаем 10 итераций для теста)
        for i in range(10):
            for recipient in ['abuse@telegram.org', 'support@telegram.org']:
                msg_text = random.choice(MESSAGES).format(target=target)
                msg = MIMEText(msg_text)
                msg['Subject'] = random.choice(SUBJECTS)
                msg['From'] = MY_EMAIL
                msg['To'] = recipient
                
                server.send_message(msg)
                success += 1
            
            time.sleep(2) # Пауза между письмами, чтоб почта не сдохла
            
        server.quit()
        bot.send_message(message.chat.id, f"✅ **ЦИКЛ ЗАВЕРШЕН!**\nОтправлено {success} уникальных жалоб.\nТвоя почта p.st.v@mail.ru отработала штатно.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}\nВозможно, Mail.ru временно заблокировал отправку за спам.")

# --- МОДУЛЬ OSINT ---
@bot.message_handler(func=lambda m: m.text == "🔍 ГЛУБОКИЙ OSINT")
def osint_menu(message):
    bot.send_message(message.chat.id, "🎯 Введи номер или ник. Также рекомендую [Глаз Бога](https://t.me/EyeGods_Bot) для глубокого поиска.")
    bot.register_next_step_handler(message, osint_run)

def osint_run(message):
    val = message.text
    res = f"👤 **АНАЛИЗ:** `{val}`\n\n├ [VK Search](https://vk.com/search?c%5Bq%5D={val})\n└ [Google Dorks](https://www.google.com/search?q=%22{val}%22)"
    bot.send_message(message.chat.id, res, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
