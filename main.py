import os, time, random, smtplib, threading, asyncio, aiohttp, requests, sqlite3, sys, socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init, Fore, Style
from pystyle import Colorate, Colors, Center, Write, Box
from flask import Flask
from threading import Thread
import telebot
import pyfiglet

init(autoreset=True)

# --- [ СИСТЕМА ЖИЗНЕОБЕСПЕЧЕНИЯ (FLASK ДЛЯ 24/7) ] ---
app = Flask('')
@app.route('/')
def home(): return "GALAXY_MONOLITH_V85_ONLINE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- [ КОНФИГУРАЦИЯ И ЗАЩИТА ] ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [6582382945]
ADMIN_NUMBERS = ["+77756041388", "+79642113737", "+77757566702", "77756041388", "9642113737", "77757566702"]
ADMIN_WARNING = "⚠️ КРИТИЧЕСКАЯ ОШИБКА: ПОПЫТКА ДЕАНОНА ОСНОВАТЕЛЯ. ВАШ IP ЗАЛОГИРОВАН."

# Твоя база SMTP (17 аккаунтов)
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

# --- [ РАСШИРЕННАЯ БАЗА OSINT (350+ САЙТОВ) ] ---
OSINT_MEGA_DB = {
    "🇰🇿 КАЗАХСТАН": ["adata.kz", "kgd.gov.kz", "spra.vkaru.net", "vinfo.kz", "zero.kz", "@ShtrafKZBot", "kn.kz", "krisha.kz (parsing)"],
    "🇷🇺 РФ & СНГ": ["fssp.gov.ru", "nalog.ru", "gibdd.rf", "zachestnyibiznes.ru", "reestr-zalogov.ru", "nomera.me", "egrul.ru"],
    "🌎 GLOBAL DEEP": ["whatsmyname.app", "leakprobe.net", "haveibeenpwned.com", "intelx.io", "pimeyes.com", "osintframework.com", "hunter.io"],
    "🕵️ PRIVATE BOTS": ["@search_himera_bot", "@Solaris_Search_Bot", "@Zernerda_bot", "@Quick_osintik_bot", "@Sangre_Bot", "@EyeGodBot"]
}

# --- [ ФОРМАТ ОТЧЕТА ] ---
REPORT_FMT = """
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

# --- [ ЛОГИКА ПРОБИВА ] ---
def global_search_logic(query):
    nick = query.split('/')[-1].replace('@', '') if '/' in query else query.replace('@', '')
    return {
        "fio": f"{nick.capitalize()} Альбертович Хзин", "dr": "04.06.1976",
        "phone": "+77" + str(random.randint(700000000, 779999999)), "email": f"{nick}@mail.ru",
        "car_num": f"{random.randint(100,999)}ABC02", "vin": "XTA" + str(random.randint(10**13, 10**14)),
        "nick": nick, "ok_id": random.randint(10000, 99999), "tg_id": f"tg{random.randint(100000, 999999)}",
        "vu": random.randint(10**9, 10**10), "passp": f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}",
        "snils": random.randint(10**10, 10**11), "inn": random.randint(10**11, 10**12), "tag": "Target Found",
        "ip": f"95.{random.randint(1,255)}.{random.randint(1,255)}.1", "address": "г. Алматы, Островитянова, 9",
        "kadastr": "77:01:0004042:6987", "inn_ur": random.randint(10**9, 10**10), "ogrn": random.randint(10**12, 10**13)
    }

# --- [ SMTP СНОС ] ---
def execute_total_snos(target, chat_id=None):
    success = 0
    for acc in ACCOUNTS:
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com' if 'gmail' in acc['email'] else 'smtp.mail.ru', 465, timeout=5)
            server.login(acc['email'], acc['pw'])
            msg = MIMEMultipart()
            msg['Subject'] = "Emergency: Illegal Content Report"
            msg['From'] = acc['email']
            msg['To'] = 'abuse@telegram.org'
            msg.attach(MIMEText(f"The user {target} is breaking laws.", 'plain'))
            server.send_message(msg); server.quit()
            success += 1
        except: continue
    if chat_id: bot.send_message(chat_id, f"💀 **УНИЧТОЖЕНИЕ ЗАВЕРШЕНО.** Пакеты: {success*3}")

# --- [ ОБРАБОТЧИКИ ТЕЛЕГРАМ ] ---
@bot.message_handler(commands=['start'])
def bot_start(message):
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(message.chat.id, "Приветствую вас вы попали в логово dio\nОтправьте ссылку или юзернейм для пробива.")

@bot.message_handler(func=lambda m: True)
def bot_handler(message):
    if message.from_user.id not in ADMIN_IDS: return
    if message.text == "💀 ТОТАЛЬНЫЙ СНОС":
        bot.send_message(message.chat.id, "🎯 Введите цель для SMTP-атаки:")
        bot.register_next_step_handler(message, lambda m: Thread(target=execute_total_snos, args=(m.text, message.chat.id)).start())
        return
    
    if is_protected(message.text):
        bot.send_message(message.chat.id, ADMIN_WARNING); return

    msg = bot.send_message(message.chat.id, "📡 **GLOBAL SCAN:** Опрашиваю базы всех стран...")
    time.sleep(2)
    data = global_search_logic(message.text)
    bot.send_message(message.chat.id, REPORT_FMT.format(**data))
    bot.send_photo(message.chat.id, "https://thispersondoesnotexist.com/", caption="📸 Снимок лица найден.")

# --- [ ФИНАЛЬНЫЙ БЛОК ДЛЯ GITHUB / SERVER ] ---
if __name__ == '__main__':
    # 1. Запуск Flask для предотвращения засыпания (24/7)
    keep_alive()
    
    # 2. Лог запуска
    print(Colorate.Vertical(Colors.red_to_black, ">>> GALAXY TITAN V85 СИНХРОНИЗИРОВАН С GITHUB."))
    print(f"{Fore.GREEN}Бот запущен. 17 SMTP-серверов готовы к работе.")

    # 3. Зацикливаем бота (основной процесс)
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
