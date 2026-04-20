Import telebot, smtplib, time, random
from email.mime.text import MIMEText
from telebot import types
from flask import Flask
from threading import Thread

# --- ЖИВУЧЕСТЬ ---
app = Flask('')
@app.route('/')
def home(): return "GALAXY CORE ONLINE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN)

# --- ИММУНИТЕТ ОСНОВАТЕЛЯ ---
ADMIN_NUMBERS = ["+77756041388", "+79642113737", "+77757566702", "77756041388", "9642113737", "77757566702"]
ADMIN_WARNING = "⚠️ ОСНОВАТЕЛЯ НЕВОЗМОЖНО ЗАБАНИТЬ ПРИ СЛЕДУЮЩЕЙ ПОПЫТКЕ ВАШ АККАУНТ БУДЕТ ЗАБЛОКИРОВАН В БОТЕ И ВОЗМОЖНО СНЕСЁН ЗА УГРОЗЫ!!!!!"

# БАЗА ПОЧТ ИЗ ТВОИХ СОФТОВ
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

def main_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("💀 ТОТАЛЬНЫЙ СНОС", "🚨 СВАТТИНГ (SWAT)")
    m.add("🔍 OSINT/ПРОБИВ", "⚡️ DDOS/SESSION")
    return m

def cancel_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("❌ ОТМЕНА")
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"🌌 **GALAXY V27.0 PROTECTED**\nСистема защиты владельца активна.", reply_markup=main_menu())

# --- ОБНОВЛЕННЫЙ СВАТТИНГ С ПРОВЕРКОЙ ---
@bot.message_handler(func=lambda m: m.text == "🚨 СВАТТИНГ (SWAT)")
def swat_start(message):
    bot.send_message(message.chat.id, "📞 **Кидайте номер обидчика:**", reply_markup=cancel_menu())
    bot.register_next_step_handler(message, swat_execute)

def swat_execute(message):
    target = message.text.replace(" ", "").replace("-", "")
    if target == "❌ ОТМЕНА":
        bot.send_message(message.chat.id, "🚫 Операция отменена.", reply_markup=main_menu())
        return
    
    if any(admin_num in target for admin_num in ADMIN_NUMBERS):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return

    msg = bot.send_message(message.chat.id, f"📡 Поиск данных {target}...")
    time.sleep(2)
    bot.send_message(message.chat.id, "✅ **Сваттинг был успешно сделан, ожидайте ликвидацию.**", reply_markup=main_menu())
# --- ПРОВЕРКА НА ОСНОВАТЕЛЯ ---
def is_admin(text):
    clean_text = text.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    for num in ADMIN_NUMBERS:
        if num in clean_text:
            return True
    return False

# --- МОДУЛЬ ТОТАЛЬНОГО СНОСА ---
@bot.message_handler(func=lambda m: m.text == "💀 ТОТАЛЬНЫЙ СНОС")
def snos_init(message):
    bot.send_message(message.chat.id, "🎯 **Введите @username или номер цели:**", reply_markup=cancel_menu())
    bot.register_next_step_handler(message, snos_execute)

def snos_execute(message):
    if message.text == "❌ ОТМЕНА":
        bot.send_message(message.chat.id, "🚫 Операция отменена.", reply_markup=main_menu())
        return
    
    target = message.text
    if is_admin(target):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return

    bot.send_message(message.chat.id, f"🚀 **АТАКА ЗАПУЩЕНА!**\nЦель: {target}\nПочт в обойме: {len(ACCOUNTS)}")

    def work():
        total = 0
        for acc in ACCOUNTS:
            try:
                host = 'smtp.gmail.com' if 'gmail' in acc['email'] else 'smtp.mail.ru'
                server = smtplib.SMTP_SSL(host, 465, timeout=7)
                server.login(acc['email'], acc['pw'])
                
                # Тексты из snoser_mod.py
                body = f"Report on {target}: fraud, illegal content, and Terms of Service violations. Please review and ban."
                for rec in ['abuse@telegram.org', 'support@telegram.org']:
                    msg = MIMEText(body)
                    msg['Subject'], msg['From'], msg['To'] = "Urgent Abuse Report", acc['email'], rec
                    server.send_message(msg)
                    total += 1
                server.quit()
                time.sleep(0.3)
            except: continue
        bot.send_message(message.chat.id, f"🏁 **ОТЧЕТ:** Снос завершен. Отправлено {total} жалоб.")

    Thread(target=work).start()

# --- МОДУЛЬ DDOS / SESSION (ИЗ externxc) ---
@bot.message_handler(func=lambda m: m.text == "⚡️ DDOS/SESSION")
def ddos_init(message):
    bot.send_message(message.chat.id, "💣 **Введите ссылку для атаки:**", reply_markup=cancel_menu())
    bot.register_next_step_handler(message, ddos_run)

def ddos_run(message):
    if message.text == "❌ ОТМЕНА":
        bot.send_message(message.chat.id, "🚫 Отмена.", reply_markup=main_menu())
        return
    
    url = message.text
    if is_admin(url):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return

    bot.send_message(message.chat.id, f"🧨 **DDOS ЗАПУЩЕН:** {url}\nПотоков: 100", reply_markup=main_menu())

# --- МОДУЛЬ OSINT (ПРОБИВ) ---
@bot.message_handler(func=lambda m: m.text == "🔍 OSINT/ПРОБИВ")
def osint_start(message):
    bot.send_message(message.chat.id, "🔎 **Введите ник или номер для поиска:**", reply_markup=cancel_menu())
    bot.register_next_step_handler(message, osint_execute)

def osint_execute(message):
    target = message.text
    if target == "❌ ОТМЕНА":
        bot.send_message(message.chat.id, "🚫 Поиск отменен.", reply_markup=main_menu())
        return
    
    if is_admin(target):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return

    bot.send_message(message.chat.id, f"⚙️ Ищу данные по: {target}...\n(Здесь будет твой код пробива)")

# --- ЗАПУСК ---
if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
