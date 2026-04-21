import os, time, random, smtplib, threading, requests, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init, Fore
from pystyle import Colorate, Colors, Center
from flask import Flask
from threading import Thread
import telebot

init(autoreset=True)

# --- [ СЕРВЕР ДЛЯ RENDER (24/7) ] ---
app = Flask('')
@app.route('/')
def home(): return "GALAXY_MONOLITH_V100_ULTIMATUM_ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- [ КОНФИГУРАЦИЯ ] ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN)
ADMIN_IDS = [6582382945]
ADMIN_NUMBERS = ["+77756041388", "+79642113737", "+77757566702", "77756041388", "9642113737", "77757566702"]

# Твои 17 аккаунтов SMTP
ACCOUNTS = [
    {'email': 'p.st.v@mail.ru', 'pw': 'itmsluvppzoxbtyi'}, {'email': 'qstkennethadams388@gmail.com', 'pw': 'itpz jkrh mtwp escx'},
    {'email': 'usppaullewis171@gmail.com', 'pw': 'lpiy xqwi apmc xzmv'}, {'email': 'ftkgeorgeanderson367@gmail.com', 'pw': 'okut ecjk hstl nucy'},
    {'email': 'nieedwardbrown533@gmail.com', 'pw': 'wvig utku ovjk appd'}, {'email': 'h56400139@gmail.com', 'pw': 'byrl egno xguy ksvf'},
    {'email': 'den.kotelnikov220@gmail.com', 'pw': 'xprw tftm lldy ranp'}, {'email': 'trevorzxasuniga214@gmail.com', 'pw': 'egnr eucw jvxg jatq'},
    {'email': 'dellapreston50@gmail.com', 'pw': 'qoit huon rzsd eewo'}, {'email': 'neilfdhioley765@gmail.com', 'pw': 'rgco uwiy qrdc gvqh'},
    {'email': 'hhzcharlesbaker201@gmail.com', 'pw': 'mcxq vzgm quxy smhh'}, {'email': 'samuelmnjassey32@gmail.com', 'pw': 'lgct cjiw nufr zxjg'},
    {'email': 'allisonikse1922@gmail.com', 'pw': 'tozo xrzu qndn mwuq'}, {'email': 'corysnja1996@gmail.com', 'pw': 'pfjk ocvn luvt rzly'},
    {'email': 'huyznaet06@gmail.com', 'pw': 'cyeb pnyi ctpj xxdx'}, {'email': 'alabuga793@gmail.com', 'pw': 'tzuk rehw syaw ozme'},
    {'email': 'editt134@gmail.com', 'pw': 'zswk msqr rjrw dtwq'}
]

# --- [ ШАБЛОНЫ ] ---
REPORT_TEMPLATE = """
Приветствую вас вы попали в логово dio 

🕵️ Личность:
{fio} {dr} - ФИО

📲 Контакты:
{phone} – номер телефона
{email} – email

🚘 Транспорт:
{car_num} – номер автомобиля
{vin} – VIN автомобиля

💬 Социальные сети:
vk.com/{nick} – Вконтакте
tiktok.com/@{nick} – Tiktok
instagram.com/{nick} – Instagram
ok.ru/profile/{ok_id} – Одноклассники

📺 Telegram:
{nick}, {tg_id} – логин или ID

📄 Документы:
/vu {vu} – водительские права
/passport {passp} – паспорт
/snils {snils} – СНИЛС
/inn {inn} – ИНН

🌐 Онлайн-следы:
/tag {tag} – поиск по телефонным книгам
{nick}.com или {ip} – домен или IP

🏚 Недвижимость:
{address}
{kadastr} - кадастровый номер

🏢 Юридическое лицо:
/inn {inn_ur} – ИНН
{ogrn} – ОГРН или ОГРНИП

📸 Отправьте лицо человека, чтобы попробовать найти его.
"""

# --- [ ЛОГИКА ] ---
def is_protected(text):
    clean = str(text).replace("+", "").replace(" ", "").replace("-", "")
    return any(num.replace("+", "") in clean for num in ADMIN_NUMBERS)

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.from_user.id not in ADMIN_IDS: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 OSINT (V100)", "💀 ТОТАЛЬНЫЙ СНОС")
    markup.add("🚨 SWAT (ВЫЗОВ)", "💥 СНОС СЕССИИ")
    bot.send_message(message.chat.id, "🛰 **GALAXY MONOLITH V100.0 ULTIMATUM**\nБригада на месте. Выбирай цель.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_commands(message):
    if message.from_user.id not in ADMIN_IDS: return
    
    if message.text == "🔍 OSINT (V100)":
        bot.send_message(message.chat.id, "🔎 Отправьте ссылку или данные:")
        bot.register_next_step_handler(message, run_osint)
    elif message.text == "💀 ТОТАЛЬНЫЙ СНОС":
        bot.send_message(message.chat.id, "🎯 Введите @username или номер:")
        bot.register_next_step_handler(message, run_snos)
    elif message.text == "🚨 SWAT (ВЫЗОВ)":
        bot.send_message(message.chat.id, "📞 Введите адрес объекта:")
        bot.register_next_step_handler(message, lambda m: bot.send_message(message.chat.id, "🚨 **СИГНАЛ ПЕРЕДАН.** Группа выехала."))
    elif message.text == "💥 СНОС СЕССИИ":
        bot.send_message(message.chat.id, "📲 Введите номер для Logout Loop:")
        bot.register_next_step_handler(message, lambda m: bot.send_message(message.chat.id, "💥 **SESSION DESTROYED.** Цель вылетела из аккаунта."))

def run_osint(message):
    if is_protected(message.text):
        bot.send_message(message.chat.id, "⚠️ ЗАЩИТА DIO."); return
    
    nick = message.text.split('/')[-1].replace('@', '') if '/' in message.text else message.text.replace('@', '')
    data = {
        "fio": f"{nick.capitalize()} Альбертович Хзин", "dr": "04.06.1976",
        "phone": "+7" + str(random.randint(7070000000, 7779999999)), "email": f"{nick}@mail.ru",
        "car_num": "В395ОК199", "vin": "XTA" + str(random.randint(10**13, 10**14)),
        "nick": nick, "ok_id": "58460", "tg_id": f"tg{random.randint(100000, 999999)}",
        "vu": "1234567890", "passp": "1234 567890", "snils": "12345678901", "inn": "123456789012",
        "tag": "Хирург", "ip": "95.161.22.1", "address": "Москва, Островитянова, 9к4",
        "kadastr": "77:01:0004042:6987", "inn_ur": "2540214547", "ogrn": "1107449004464"
    }
    bot.send_message(message.chat.id, REPORT_TEMPLATE.format(**data))
    bot.send_photo(message.chat.id, "https://thispersondoesnotexist.com/", caption="📸 Найдено в FaceID (V100)")

def run_snos(message):
    bot.send_message(message.chat.id, f"💀 **SMTP ATTACK START:** Использую 17 серверов...")
    # Тут логика SMTP из прошлых версий
    bot.send_message(message.chat.id, f"✅ Аккаунт {message.text} заблокирован в системе очередей.")

# --- [ ВЕС ФАЙЛА 50МБ+ ДЛЯ GITHUB ] ---
FAT_BLOCK = "DIO_ULTIMATUM_V100" * (1024 * 1024 * 50 // 18)

if __name__ == '__main__':
    keep_alive()
    print(">>> GALAXY V100.0 ULTIMATUM LOADED.")
    bot.polling(none_stop=True)
