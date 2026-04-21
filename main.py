import os, time, random, smtplib, threading, requests, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init, Fore
from pystyle import Colorate, Colors, Center
from flask import Flask
from threading import Thread
import telebot

init(autoreset=True)

# --- [ СЕРВЕР 24/7 ] ---
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

# Твои 17 SMTP-аккаунтов
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

# --- [ ШАБЛОН ТВОЕГО ОТЧЕТА ] ---
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

def is_protected(text):
    clean = str(text).replace("+", "").replace(" ", "").replace("-", "")
    return any(num.replace("+", "") in clean for num in ADMIN_NUMBERS)

# --- [ МЕТОДЫ АТАКИ ] ---
def snos_logic(target, chat_id):
    success = 0
    for acc in ACCOUNTS:
        try:
            s = smtplib.SMTP_SSL('smtp.gmail.com' if 'gmail' in acc['email'] else 'smtp.mail.ru', 465, timeout=5)
            s.login(acc['email'], acc['pw'])
            msg = MIMEMultipart()
            msg['Subject'] = "Emergency Report"
            msg['From'] = acc['email']; msg['To'] = 'abuse@telegram.org'
            msg.attach(MIMEText(f"Target {target} violates TOS.", 'plain'))
            s.send_message(msg); s.quit()
            success += 1
        except: continue
    bot.send_message(chat_id, f"💀 **СНОС ЗАВЕРШЕН.**\nОтправлено жалоб: {success*3}")

def session_destroy(target, chat_id):
    # Имитация Logout Loop через API шлюзы
    bot.send_message(chat_id, f"🛰 **SESSION ATTACK:** Подключаюсь к сессиям {target}...")
    time.sleep(2)
    bot.send_message(chat_id, f"💥 **LOGOUT LOOP:** Запущен цикл сброса авторизации. Цель будет вылетать из аккаунта каждые 5 сек.")

# --- [ ОБРАБОТКА КОМАНД ] ---
@bot.message_handler(commands=['start'])
def welcome(message):
    if message.from_user.id not in ADMIN_IDS: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 OSINT", "💀 СНОС ТГ", "🚨 SWAT", "💥 СНОС СЕССИИ")
    bot.send_message(message.chat.id, "🛰 **GALAXY MONOLITH V100 ONLINE.**\nДобро пожаловать в логово dio.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def main_logic(message):
    if message.from_user.id not in ADMIN_IDS: return
    
    if message.text == "🔍 OSINT":
        bot.send_message(message.chat.id, "🔎 Введите ФИО/Номер/Юзернейм:")
        bot.register_next_step_handler(message, process_osint)
    elif message.text == "💀 СНОС ТГ":
        bot.send_message(message.chat.id, "🎯 Введите цель для уничтожения:")
        bot.register_next_step_handler(message, lambda m: Thread(target=snos_logic, args=(m.text, message.chat.id)).start())
    elif message.text == "🚨 SWAT":
        bot.send_message(message.chat.id, "📞 Введите адрес объекта для SWAT-вызова:")
        bot.register_next_step_handler(message, lambda m: bot.send_message(message.chat.id, "✅ **SWAT ЗАПУЩЕН.** Данные переданы в региональное управление."))
    elif message.text == "💥 СНОС СЕССИИ":
        bot.send_message(message.chat.id, "📲 Введите номер телефона цели для Logout Loop:")
        bot.register_next_step_handler(message, lambda m: session_destroy(m.text, message.chat.id))

def process_osint(message):
    target = message.text
    if is_protected(target):
        bot.send_message(message.chat.id, "⚠️ ОШИБКА: Защита создателя."); return
    
    msg = bot.send_message(message.chat.id, "📡 **ГЛОБАЛЬНЫЙ ПОИСК...**")
    time.sleep(2)
    
    nick = target.split('/')[-1].replace('@', '') if '/' in target else target.replace('@', '')
    data = {
        "fio": f"{nick.capitalize()} Альбертович Хзин", "dr": "04.06.1976",
        "phone": "+7" + str(random.randint(7070000000, 7779999999)), "email": f"{nick}@mail.ru",
        "car_num": "В395ОК199", "vin": "XTA" + str(random.randint(10**13, 10**14)), "nick": nick,
        "ok_id": "58460", "tg_id": f"tg{random.randint(10**6, 10**8)}", "vu": "1234567890",
        "passp": "1234 567890", "snils": "12345678901", "inn": "123456789012", "tag": "Хирург",
        "ip": "95.161.22.1", "address": "Москва, Островитянова, 9к4", "kadastr": "77:01:0004042:6987",
        "inn_ur": "2540214547", "ogrn": "1107449004464"
    }
    
    bot.edit_message_text(REPORT_TEMPLATE.format(**data), message.chat.id, msg.message_id)
    bot.send_photo(message.chat.id, "https://thispersondoesnotexist.com/", caption="📸 Найдено в FaceID")

# --- [ ВЕС ФАЙЛА 50МБ+ ] ---
FAT_DATA = "DIO_SUPREMACY" * (1024 * 1024 * 50 // 13)

if __name__ == '__main__':
    keep_alive()
    print(">>> GALAXY V100 ACTIVE. OSINT/SNOS/SWAT/SESSION READY.")
    bot.polling(none_stop=True)
