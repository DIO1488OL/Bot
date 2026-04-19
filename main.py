import telebot
import requests
import phonenumbers
from telebot import types
from phonenumbers import carrier, geocoder
from flask import Flask
from threading import Thread

# --- МИНИ-СЕРВЕР (АНТИ-СОН) ---
app = Flask('')
@app.route('/')
def home():
    return "Status: Online"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- АКТУАЛЬНЫЙ ТОКЕН ---
TOKEN = '8712209115:AAE4oAGeUKjNpybxUPFNP-UwkfWJCq6AqGg'
bot = telebot.TeleBot(TOKEN)

# --- ГЛАВНОЕ МЕНЮ ---
def main_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("💀 СНОСЕР (ВАВИЛОН)", "🔍 ГЛУБОКИЙ OSINT")
    m.add("📂 ПРИВАТНЫЕ МАНУАЛЫ", "⚙️ ТЕРМИНАТОР СЕССИЙ")
    m.add("🧨 СВАТТИНГ / ДОСТАВКИ", "🛡 АНОНИМНОСТЬ")
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 **GALAXY ANNIHILATOR V7.5 HYBRID**\n\nКонфликты устранены, OSINT-модули обновлены до кликабельных ссылок.", reply_markup=main_menu(), parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    t = message.text
    cid = message.chat.id

    if t == "💀 СНОСЕР (ВАВИЛОН)":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Снести ВК", callback_data="snos_vk"))
        kb.add(types.InlineKeyboardButton("Снести ТГ Канал", callback_data="snos_tg"))
        bot.send_message(cid, "🧨 **ВЫБЕРИ ТИП АТАКИ:**", reply_markup=kb, parse_mode='Markdown')

    elif t == "🔍 ГЛУБОКИЙ OSINT":
        bot.send_message(cid, "🎯 **ВВЕДИ ЦЕЛЬ:**\nНомер (с +7...) или Никнейм (без @)")
        bot.register_next_step_handler(message, run_osint)

    elif t == "📂 ПРИВАТНЫЕ МАНУАЛЫ":
        bot.send_message(cid, "📚 **БАЗА ЗНАНИЙ:**\n\n1. **Delfin (Lvl 3):** Социальная инженерия + RAT.\n2. **Shtosh:** Деанон через курьеров и чеки.", parse_mode='Markdown')

    elif t == "⚙️ ТЕРМИНАТОР СЕССИЙ":
        bot.send_message(cid, "⚙️ **ИНСТРУКЦИЯ:** Отправь тикет 'Stolen Device' в поддержку ТГ. В поле IP укажи адрес цели из логгера. Это принудительно завершит его сеансы.")

    elif t == "🧨 СВАТТИНГ / ДОСТАВКИ":
        bot.send_message(cid, "🧨 **МЕТОДЫ:**\n- Анонимные заказы через левые SIM.\n- Использование 5ymail через TOR для анонимных писем.")

    elif t == "🛡 АНОНИМНОСТЬ":
        bot.send_message(cid, "🛡 **СОВЕТ:** Никогда не заходи в админку Render без VPN. Юзай Double VPN для работы с панелью бота.")

# --- УЛУЧШЕННЫЙ OSINT (ССЫЛКИ) ---
def run_osint(message):
    val = message.text
    cid = message.chat.id
    
    if val.startswith('+'):
        try:
            p = phonenumbers.parse(val)
            c = carrier.name_for_number(p, 'ru')
            r = geocoder.description_for_number(p, 'ru')
            
            res = (
                f"📱 **АНАЛИЗ НОМЕРА:** `{val}`\n"
                f"├ Оператор: {c if c else 'Неизвестен'}\n"
                f"└ Регион: {r if r else 'Неизвестен'}\n\n"
                f"🔗 **БЫСТРЫЙ ПРОБИВ:**\n"
                f"├ [TrueCaller Web](https://www.truecaller.com/search/ru/{val})\n"
                f"├ [Проверить WhatsApp](https://wa.me/{val.replace('+', '')})\n"
                f"└ [Telegram Поиск](tg://resolve?phone={val.replace('+', '')})"
            )
            bot.send_message(cid, res, parse_mode='Markdown', disable_web_page_preview=True)
        except:
            bot.send_message(cid, "❌ Кривой формат номера!")
    else:
        res = (
            f"👤 **АНАЛИЗ НИКА:** `{val}`\n\n"
            f"🔗 **ПРЯМЫЕ ССЫЛКИ:**\n"
            f"├ [Поиск в VK](https://vk.com/search?c%5Bq%5D={val}&c%5Bsection%5D=people)\n"
            f"├ [Поиск в Instagram](https://www.instagram.com/{val}/)\n"
            f"└ [Google Dorks](https://www.google.com/search?q=%22{val}%22)"
        )
        bot.send_message(cid, res, parse_mode='Markdown', disable_web_page_preview=True)

# --- ОБРАБОТКА ИНЛАЙН КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "snos_vk":
        bot.send_message(call.message.chat.id, "📝 **ЖАЛОБА ВК:** 'Прошу заблокировать за нарушение правил сообщества (п. 5.2 - спам/боты)'.")
    elif call.data == "snos_tg":
        bot.send_message(call.message.chat.id, "📝 **ЖАЛОБА ТГ:** 'Report for doxing, harassment and illegal content'.")

if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
