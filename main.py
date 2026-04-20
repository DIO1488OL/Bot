import telebot, smtplib, time, random
from email.mime.text import MIMEText
from telebot import types
from flask import Flask
from threading import Thread

# --- SYSTEM ---
app = Flask('')
@app.route('/')
def home(): return "SYSTEM_ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN)

# --- DATABASE ---
ADMIN_NUMBERS = ["+77756041388", "+79642113737", "+77757566702", "77756041388", "9642113737", "77757566702"]
ADMIN_WARNING = "⚠️ ОСНОВАТЕЛЯ НЕВОЗМОЖНО ЗАБАНИТЬ ПРИ СЛЕДУЮЩЕЙ ПОПЫТКЕ ВАШ АККАУНТ БУДЕТ ЗАБЛОКИРОВАН В БОТЕ И ВОЗМОЖНО СНЕСЁН ЗА УГРОЗЫ!!!!!"

ACCOUNTS = [
    {'email': 'p.st.v@mail.ru', 'pw': 'itmsluvppzoxbtyi'},
    {'email': 'qstkennethadams388@gmail.com', 'pw': 'itpz jkrh mtwp escx'},
    {'email': 'usppaullewis171@gmail.com', 'pw': 'lpiy xqwi apmc xzmv'},
    {'email': 'ftkgeorgeanderson367@gmail.com', 'pw': 'okut ecjk hstl nucy'},
    {'email': 'nieedwardbrown533@gmail.com', 'pw': 'wvig utku ovjk appd'},
    {'email': 'h56400139@gmail.com', 'pw': 'byrl egno xguy ksvf'},
    {'email': 'den.kotelnikov220@gmail.com', 'pw': 'xprw tftm lldy ranp'},
    {'email': 'trevorzxasuniga214@gmail.com', 'pw': 'egnr eucw jvxg jatq'},
    {'email': 'dellapreston50@gmail.com', 'pw': 'qoit huon rzsd eewo'},
    {'email': 'neilfdhioley765@gmail.com', 'pw': 'rgco uwiy qrdc gvqh'},
    {'email': 'hhzcharlesbaker201@gmail.com', 'pw': 'mcxq vzgm quxy smhh'},
    {'email': 'samuelmnjassey32@gmail.com', 'pw': 'lgct cjiw nufr zxjg'},
    {'email': 'allisonikse1922@gmail.com', 'pw': 'tozo xrzu qndn mwuq'},
    {'email': 'corysnja1996@gmail.com', 'pw': 'pfjk ocvn luvt rzly'},
    {'email': 'huyznaet06@gmail.com', 'pw': 'cyeb pnyi ctpj xxdx'},
    {'email': 'alabuga793@gmail.com', 'pw': 'tzuk rehw syaw ozme'},
    {'email': 'editt134@gmail.com', 'pw': 'zswk msqr rjrw dtwq'}
]

def is_admin(text):
    if not text: return False
    clean = text.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
    for num in ADMIN_NUMBERS:
        if num.replace("+", "") in clean: return True
    return False

def main_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("💀 ТОТАЛЬНЫЙ СНОС", "🚨 СВАТТИНГ (SWAT)")
    m.add("🔍 OSINT/ПРОБИВ", "⚡️ DDOS/SESSION")
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🛰 **GALAXY CORE V28.0**\nСистема готова к работе.", reply_markup=main_menu())

# --- SWAT ---
@bot.message_handler(func=lambda m: m.text == "🚨 СВАТТИНГ (SWAT)")
def swat_start(message):
    bot.send_message(message.chat.id, "📞 Кидайте номер обидчика:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, swat_execute)

def swat_execute(message):
    if is_admin(message.text):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return
    bot.send_message(message.chat.id, "📡 Обработка запроса...")
    time.sleep(3)
    bot.send_message(message.chat.id, "✅ **Сваттинг был успешно сделан, ожидайте ликвидацию.**", reply_markup=main_menu())

# --- SNOS ---
@bot.message_handler(func=lambda m: m.text == "💀 ТОТАЛЬНЫЙ СНОС")
def snos_init(message):
    bot.send_message(message.chat.id, "🎯 Введите @username или номер цели:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, snos_execute)

def snos_execute(message):
    if is_admin(message.text):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return
    
    target = message.text
    bot.send_message(message.chat.id, "🚀 АТАКА ЗАПУЩЕНА", reply_markup=main_menu())

    def work():
        count = 0
        for acc in ACCOUNTS:
            try:
                host = 'smtp.gmail.com' if 'gmail' in acc['email'] else 'smtp.mail.ru'
                server = smtplib.SMTP_SSL(host, 465, timeout=5)
                server.login(acc['email'], acc['pw'])
                msg = MIMEText(f"Report: {target} violates TOS (scam/illegal content).")
                msg['Subject'], msg['From'], msg['To'] = "Abuse Report", acc['email'], 'abuse@telegram.org'
                server.send_message(msg)
                server.quit()
                count += 1
            except: continue
        bot.send_message(message.chat.id, f"🏁 Завершено. Отправлено жалоб: {count * 2}")

    Thread(target=work).start()

# --- OTHER ---
@bot.message_handler(func=lambda m: m.text == "🔍 OSINT/ПРОБИВ")
def osint_start(message):
    bot.send_message(message.chat.id, "🔎 Введите ник или номер для поиска:")

@bot.message_handler(func=lambda m: m.text == "⚡️ DDOS/SESSION")
def ddos_init(message):
    bot.send_message(message.chat.id, "💣 Введите ссылку для атаки:")

if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
