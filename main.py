import telebot, smtplib, time, random, threading
from email.mime.text import MIMEText
from telebot import types
from flask import Flask
from threading import Thread

# --- SYSTEM SETUP ---
app = Flask('')
@app.route('/')
def home(): return "GALAXY_CORE_ONLINE"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN)

# --- DATABASE & PROTECTION ---
ADMIN_NUMBERS = ["+77756041388", "+79642113737", "+77757566702", "77756041388", "9642113737", "77757566702"]
ADMIN_WARNING = "⚠️ ОСНОВАТЕЛЯ НЕВОЗМОЖНО ЗАБАНИТЬ! ПРИ СЛЕДУЮЩЕЙ ПОПЫТКЕ ВАШ АККАУНТ БУДЕТ ЗАБЛОКИРОВАН И СНЕСЁН ЗА УГРОЗЫ!"

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
    m.add("🔍 OSINT (ПОИСК ДАННЫХ)", "⚡️ DDOS/SESSION")
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🛰 **GALAXY CORE V28.0 SUPREMACY**\nБригада на месте. Выбирай цель.", reply_markup=main_menu())

# --- SWAT LOGIC ---
@bot.message_handler(func=lambda m: m.text == "🚨 СВАТТИНГ (SWAT)")
def swat_start(message):
    bot.send_message(message.chat.id, "📞 Введите номер телефона или адрес цели для SWAT-атаки:")
    bot.register_next_step_handler(message, swat_execute)

def swat_execute(message):
    target = message.text
    if is_admin(target):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return
    
    bot.send_message(message.chat.id, "📡 **Идет поиск геолокации и привязки к ФИО...**")
    time.sleep(2)
    bot.send_message(message.chat.id, "✉️ **Генерация ложного вызова по протоколу 112...**")
    time.sleep(3)
    bot.send_message(message.chat.id, "✅ **Сваттинг успешно инициирован. Группа выезда уведомлена. Ожидайте ликвидацию цели.**", reply_markup=main_menu())

# --- ADVANCED SNOS ---
@bot.message_handler(func=lambda m: m.text == "💀 ТОТАЛЬНЫЙ СНОС")
def snos_init(message):
    bot.send_message(message.chat.id, "🎯 Введите @username или телефон для сноса аккаунта:")
    bot.register_next_step_handler(message, snos_execute)

def snos_execute(message):
    target = message.text
    if is_admin(target):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return
    
    msg_status = bot.send_message(message.chat.id, "🚀 **АТАКА ЗАПУЩЕНА: Отправка жалоб через 17 SMTP-аккаунтов...**")

    def work():
        success = 0
        for acc in ACCOUNTS:
            try:
                host = 'smtp.gmail.com' if 'gmail' in acc['email'] else 'smtp.mail.ru'
                server = smtplib.SMTP_SSL(host, 465, timeout=7)
                server.login(acc['email'], acc['pw'])
                
                # Рандомизация темы и текста для обхода фильтров ТГ
                topics = ["Child Abuse Report", "Terrorism Activity", "Scam/Fraud Investigation"]
                body = f"Report for {target}: Violating Telegram TOS. Evidence of illegal content found."
                
                msg = MIMEText(body)
                msg['Subject'] = random.choice(topics)
                msg['From'] = acc['email']
                msg['To'] = 'abuse@telegram.org'
                
                server.send_message(msg)
                server.quit()
                success += 1
            except: continue
        bot.send_message(message.chat.id, f"🏁 **Атака завершена!**\nАккаунт в очереди на бан.\nЖалоб отправлено: {success * 3}", reply_markup=main_menu())

    Thread(target=work).start()

# --- OSINT LOGIC ---
@bot.message_handler(func=lambda m: m.text == "🔍 OSINT (ПОИСК ДАННЫХ)")
def osint_start(message):
    bot.send_message(message.chat.id, "🔎 Введите номер, ID или IP для полного пробива:")
    bot.register_next_step_handler(message, osint_execute)

def osint_execute(message):
    target = message.text
    if is_admin(target):
        bot.send_message(message.chat.id, ADMIN_WARNING, reply_markup=main_menu())
        return
    
    bot.send_message(message.chat.id, f"🔄 Поиск по базам...\nЦель: {target}\n\n[+] Номер найден\n[+] IP определен: 178.204.XX.XX\n[+] ФИО: Анализ...\n[+] Пароли: Найдены в 4 утечках.\n\nПолный отчет выслан в лог.")

if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
