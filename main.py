import telebot
from database import LocalDB
# Тут можно импортировать доп. модули из tools.py

TOKEN = '8783661558:AAG_kN1t_34kui6wj0WyInJA5frqApRT1r0'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6582382945

@bot.message_handler(commands=['start'])
def welcome(m):
    if m.from_user.id != ADMIN_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔎 Поиск по базам", "🌐 Внешний OSINT")
    bot.send_message(m.chat.id, "🔱 **FRAMEWORK X GITHUB EDITION** 🔱", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(m):
    if m.from_user.id != ADMIN_ID: return
    
    if m.text == "🔎 Поиск по базам":
        msg = bot.send_message(m.chat.id, "Введите запрос (ФИО/Номер/Почта):")
        bot.register_next_step_handler(msg, run_search)

def run_search(m):
    results = LocalDB.search(m.text)
    if not results:
        bot.send_message(m.chat.id, "❌ Ничего не найдено.")
    else:
        # Отправляем первые 5 совпадений, чтобы не спамить
        for res in results[:5]:
            bot.send_message(m.chat.id, f"<code>{res}</code>", parse_mode='html')

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
