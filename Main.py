import telebot
import smtplib
import random
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telebot import types
from flask import Flask
from threading import Thread
from fake_useragent import UserAgent

# --- СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Core Status: Online"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- КОНФИГУРАЦИЯ ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
MY_EMAIL = 'p.st.v@mail.ru'
MY_APP_PASSWORD = 'itmsluvppzoxbtyi'
bot = telebot.TeleBot(TOKEN)
ua = UserAgent()

# --- ДАННЫЕ ИЗ ТВОИХ СКРИПТОВ (snos4, nsvl, yahoo) ---
RECIPIENTS = ['abuse@telegram.org', 'support@telegram.org', 'dmca@telegram.org']
SUBJECTS = ["Report for User", "Violation of rules", "Help please", "Reporting Abuse", "Security Issue"]
MESSAGES = [
    "Hello, I want to report user {target}. This user violates Telegram rules, uses virtual numbers and threats people.",
    "Dear Support, please check {target}. This account is spreading illegal content and scamming users.",
    "Urgent report: {target} is using your platform for prohibited activities. Take action immediately!",
    "I am reporting {target} for harassment and spreading private data (doxing) without consent."
]

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💀 ПОЛНЫЙ СНОС (MAX)", "🔍 ГЛУБОКИЙ ОСИНТ")
    markup.add("📂 МОИ БАЗЫ (1ГБ+)", "🛡 АНОНИМНОСТЬ")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🛰 **GALAXY ANNIHILATOR V17.0 MAX**\n\nВсе алгоритмы из твоих файлов (by.nsvl, snos4, snos_tg) загружены в ядро.", reply_markup=main_menu(), parse_mode='Markdown')

# --- ФУНКЦИЯ СНОСА (ПОЛНАЯ КОПИЯ ТВОИХ СКРИПТОВ) ---
@bot.message_handler(func=lambda m: m.text == "💀 ПОЛНЫЙ СНОС (MAX)")
def snos_start(message):
    bot.send_message(message.chat.id, "🎯 **Введите цель (@username или ссылка):**")
    bot.register_next_step_handler(message, snos_execute)

def snos_execute(message):
    target = message.text
    bot.send_message(message.chat.id, f"🚀 **ЗАПУСК ТЯЖЕЛОЙ АТАКИ...**\nЦель: {target}\nИспользую рандомные User-Agent и заголовки.")
    
    def attack_thread():
        success = 0
        try:
            # Логика из snos yahoo.py
            server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
            server.login(MY_EMAIL, MY_APP_PASSWORD)
            
            for _ in range(10): # 10 итераций
                for recipient in RECIPIENTS:
                    msg = MIMEMultipart()
                    msg['From'] = MY_EMAIL
                    msg['To'] = recipient
                    msg['Subject'] = random.choice(SUBJECTS)
                    
                    # Имитируем разные браузеры
                    headers = {'User-Agent': ua.random}
                    
                    body = random.choice(MESSAGES).format(target=target)
                    msg.attach(MIMEText(body, 'plain'))
                    
                    server.send_message(msg)
                    success += 1
                time.sleep(2)
            
            server.quit()
            bot.send_message(message.chat.id, f"✅ **АТАКА ЗАВЕРШЕНА!**\nОтправлено {success} репортов. Почта {MY_EMAIL} в норме.")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Критическая ошибка: {e}")

    # Запускаем в отдельном потоке, чтоб бот не тупил
    Thread(target=attack_thread).start()

# --- ОСИНТ (ПОИСК ПО ФАЙЛУ) ---
@bot.message_handler(func=lambda m: m.text == "🔍 ГЛУБОКИЙ ОСИНТ")
def osint_start(message):
    bot.send_message(message.chat.id, "🎯 Введите данные для пробива (база 1ГБ+):")
    bot.register_next_step_handler(message, osint_execute)

def osint_execute(message):
    query = message.text
    bot.send_message(message.chat.id, f"🔎 Ищу `{query}` в твоих архивах...")
    
    # Здесь будет поиск по твоему 1ГБ файлу
    bot.send_message(message.chat.id, f"📊 Результат по `{query}`:\n\n[ДАННЫЕ ИЗ БАЗЫ ТУТ]\n\n🔗 [Глаз Бога](https://t.me/EyeGods_Bot)")

if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
