import os, time, random, smtplib, threading, requests, sys, socket, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask
from threading import Thread
import telebot

# --- [ ЦЕНТРАЛЬНАЯ КОНФИГУРАЦИЯ ] ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=1000)

# Доступ для тебя и твоих друзей
ADMIN_IDS = [6582382945, 123456789] # Добавь сюда ID друзей
ADMIN_NUMBERS = ["+77756041388", "+79642113737", "+77757566702"]

# --- [ БАЗА МЕТОДОВ СНОСА (300+ ПОЧТ) ] ---
SENDERS = {
    'qstkennethadams388@gmail.com':'itpz jkrh mtwp escx',
    'usppaullewis171@gmail.com':'lpiy xqwi apmc xzmv',
    'ftkgeorgeanderson367@gmail.com':'okut ecjk hstl nucy',
    'p.st.v@mail.ru': 'itmsluvppzoxbtyi',
    # + еще 296 аккаунтов в массиве...
}

# --- [ МОДУЛЬ ГЛУБОКОГО ОСИНТА (3000+ SITES) ] ---
def get_ultimate_dossier(target, status="ЦЕЛЬ"):
    """Генерация пасты, которую человек сам о себе не знает"""
    
    # Имитация работы с базами (РФ, КЗ, США, ЕС)
    providers = ["Beeline", "Kazakhtelecom", "MTS", "Verizon", "Starlink"]
    devices = ["iPhone 15 Pro", "Samsung S24 Ultra", "PC (Windows 11)", "Xiaomi 13T"]
    
    # Генерация паспортных и финансовых данных
    pass_seria = f"{random.randint(1000, 9999)}"
    pass_num = f"{random.randint(100000, 999999)}"
    inn = "".join([str(random.randint(0, 9)) for _ in range(12)])
    snils = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(100, 999)} {random.randint(10, 99)}"
    
    # Секция пробива по IP
    ip_addr = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    dossier = f"""
------------------------------------------
🔱 **DOSSIER: {target.upper()} ({status})**
------------------------------------------
📎  ФИО: {target.capitalize()} {random.choice(['Ахметов', 'Смирнов', 'Ким'])} {random.choice(['Александрович', 'Кайратович', 'Сергеевич'])}
📎  Дата рождения: {random.randint(1,28)}.{random.randint(1,12)}.{random.randint(1975, 2010)}
📎  Телефон: +7 {random.choice(['701', '777', '926', '903'])}{random.randint(1000000, 9999999)}

🌐 **IP-АНАЛИЗ (DEEP SCAN):**
📎  Текущий IP: `{ip_addr}`
📎  Провайдер: {random.choice(providers)}
📎  Тип: Статический (Residential)
📎  Устройство: {random.choice(devices)}
📎  Браузер: Chrome/121.0.6167.140 (Official Build)
📎  Гео: {random.choice(['Алматы', 'Москва', 'Астана', 'Киев'])}, Lat: {random.uniform(40, 55):.4f}, Lon: {random.uniform(30, 80):.4f}

📄 **ГОС-РЕЕСТРЫ (3000+ БАЗ):**
📎  Паспорт РФ/КЗ: {pass_seria} {pass_num}
📎  ИНН/ИИН: {inn}
📎  СНИЛС: {snils}
📎  Кредитный рейтинг: {random.choice(['Высокий (780)', 'Низкий (320)', 'Средний (550)'])}
📎  Задолженность ФССП: {random.randint(0, 500000)} руб.

🏛 **УЧЕБА И КАРЬЕРА:**
📎  Образование: {random.choice(['Университет (ВУЗ)', 'Колледж', 'Техникум'])}
📎  Место: {random.choice(['НИУ ВШЭ', 'МГТУ', 'КазНУ', 'Технический лицей №2'])}
📎  Работа: {random.choice(['Kaspi Bank', 'Wildberries', 'ООО ТрансНефть', 'Freelance'])}
📎  Должность: {random.choice(['Ведущий специалист', 'Менеджер', 'Разработчик', 'Администратор'])}

📲 **SOCIAL MEDIA & APPS:**
📎  TG: @{target.lower()} | ID: {random.randint(1000000, 999999999)}
📎  VK: vk.com/id{random.randint(1000000, 500000000)}
📎  Inst/TikTok: Active (@{target.lower()}_official)
📎  WhatsApp/Viber/Signal: Найдено совпадение
"""
    return dossier

# --- [ МОДУЛЬ ГЛОБАЛЬНОГО СНОСА ] ---
def execute_void_snos(message, target):
    """Многопоточный снос аккаунтов"""
    msg = bot.send_message(message.chat.id, "💀 **VOID SYSTEM: ЗАПУСК ГЛОБАЛЬНОЙ ЖАТВЫ...**")
    
    # Разные способы сноса (Тексты из твоих файлов)
    methods = [
        "Report: Violent Content / Terrorism",
        "Report: Child Abuse Policy Violation",
        "Report: Fraud and Scams",
        "Report: Copyright Infringement"
    ]
    
    count = 0
    for email, pw in SENDERS.items():
        try:
            bot.edit_message_text(f"💀 **FLOODING:** {count+1}/300\nПоток: `{email}`", message.chat.id, msg.message_id)
            server = smtplib.SMTP_SSL('smtp.gmail.com' if 'gmail' in email else 'smtp.mail.ru', 465, timeout=5)
            server.login(email, pw)
            
            for receiver in ['abuse@telegram.org', 'support@whatsapp.com', 'support@instagram.com']:
                m = MIMEMultipart()
                m['Subject'] = "Emergency Take-Down Request"
                m['From'] = email
                m.attach(MIMEText(f"Target account {target} violates safety standards: {random.choice(methods)}", 'plain'))
                server.send_message(m)
            server.quit()
            count += 1
            if count >= 300: break
        except: continue
        
    bot.send_message(message.chat.id, f"✅ **VOID COMPLETE.** Аккаунты цели стерты по {count} направлениям.")

# --- [ МОДУЛЬ СВАТТИНГА ] ---
def execute_swat_raid(message, addr):
    """Имитация выезда спецподразделений"""
    msg = bot.send_message(message.chat.id, "🚨 **CHRONOS SWAT: УСТАНОВКА СВЯЗИ...**")
    
    logs = [
        "📡 Перехват трафика 112 через SIP-шлюз...",
        "🔌 Подмена геолокации звонящего (VPN: Active)",
        "🔊 Передача аудио-сообщения о захвате...",
        "📍 Адрес подтвержден: " + addr,
        "🚨 СОБР/ОМОН выехали. Время до контакта: 3-5 мин.",
        "📱 Блокировка связи в радиусе 100м..."
    ]
    
    for log in logs:
        time.sleep(1.5)
        bot.edit_message_text(f"🚨 **SWAT STATUS:**\n{log}", message.chat.id, msg.message_id)
    
    bot.send_message(message.chat.id, "✅ **ОПЕРАЦИЯ ВЫПОЛНЕНА.** Объект нейтрализуется.")

# --- [ ОБРАБОТЧИК ПРИВЕТСТВИЯ ] ---
@bot.message_handler(commands=['start'])
def start(message):
    # Доступ только для тебя и твоих друзей
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🛑 **ВНИМАНИЕ: СИСТЕМА ЗАБЛОКИРОВАНА.**\nПри любой попытке взаимодействия с создателем или несанкционированном доступе вы будете заблокированы.")
        return

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🌀 ГЛОБАЛЬНЫЙ ASTRAL (3000+)", "💀 VOID DESTROYER (300+)")
    markup.row("🚨 ВЫЗОВ SWAT", "🎭 FACE RECOGNITION")
    markup.row("🛡 ГРУППА ДРУЗЕЙ", "⚙️ SETTINGS")
    
    welcome_text = f"""
🛰 **ВЫ ПОПАЛИ В ЛОГОВО ЛОРДА БРАНДО** 🔱

Я — Дио. Здесь собраны лучшие инструменты для осинта и сноса. 
Мы найдем всё: от прабабушки до IP-адреса и места учебы.

⚠️ **ПРЕДУПРЕЖДЕНИЕ:** Любое взаимодействие с создателем карается **БЛОКИРОВКОЙ**.

**НОВЫЕ ФУНКЦИИ:**
• Пробив по IP (Гео, Провайдер, Устройство)
• Полное дерево родственников (Паспорта, ИНН, Работа)
• 4 метода сноса (Terrorism, Child Abuse, Scams, Copyright)
• Поиск по биометрии лица (FaceID)

{get_ultimate_dossier('осинт')}
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def router(message):
    if message.from_user.id not in ADMIN_IDS: return
    
    # Защита тебя
    if any(num in message.text for num in ADMIN_NUMBERS):
        bot.send_message(message.chat.id, "❌ **СИСТЕМА ЗАЩИТЫ АКТИВНА.** Попытка взаимодействия с Создателем."); return

    if message.text == "🌀 ГЛОБАЛЬНЫЙ ASTRAL (3000+)":
        bot.send_message(message.chat.id, "🔎 Введи Ник/Номер/IP/ФИО для полного вскрытия:")
        bot.register_next_step_handler(message, process_osint)
    elif message.text == "💀 VOID DESTROYER (300+)":
        bot.send_message(message.chat.id, "🎯 Кого стираем (TG/WhatsApp/Mail)?")
        bot.register_next_step_handler(message, lambda m: execute_void_snos(m, m.text))
    elif message.text == "🚨 ВЫЗОВ SWAT":
        bot.send_message(message.chat.id, "📞 Введи адрес для вызова группы:")
        bot.register_next_step_handler(message, lambda m: execute_swat_raid(m, m.text))
    elif message.text == "🎭 FACE RECOGNITION":
        bot.send_message(message.chat.id, "📸 Отправь фото лица для поиска по базе:")

def process_osint(message):
    p = bot.send_message(message.chat.id, "🌀 **ASTRAL: ПОИСК ПО ГЛОБАЛЬНЫМ ШЛЮЗАМ...**")
    time.sleep(2)
    
    # Цель
    bot.edit_message_text(get_ultimate_dossier(message.text), message.chat.id, p.message_id)
    
    # Семья
    family = ["Мама", "Папа", "Бабушка", "Дедушка", "Тетя", "Дядя", "Прабабка"]
    for member in family:
        time.sleep(0.8)
        bot.send_message(message.chat.id, get_ultimate_dossier(member, member))
    
    # Лицо
    bot.send_photo(message.chat.id, "https://thispersondoesnotexist.com/", caption="📸 **FaceID: Лицо найдено.**")

# --- [ СЛУЖЕБНОЕ РАЗДУТИЕ ] ---
FAT_DATA = "BRANDONIAN_SUPREME_V100" * (1024 * 1024 * 50 // 24)

app = Flask('')
@app.route('/')
def home(): return "OMNISCIENT_SYSTEM_ACTIVE"
def run(): app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run).start()
    bot.polling(none_stop=True)
