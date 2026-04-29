import os, telebot, threading, random, smtplib, time, requests, csv, json
from telethon import TelegramClient, sync
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pystyle import Colors, Colorate, Center, Write
# --- [ КОНФИГУРАЦИЯ ЛОКАЛЬНЫХ БАЗ ] ---
DB_FILES = [
    "билайн юзеры.csv",
    "государственные услуги p1.csv",
    "государственные услуги p2.csv",
    "государственные услуги p3.csv"
]

# --- [ АРХИВ ДАННЫХ: ВСЕ ССЫЛКИ И ТЕКСТЫ СОХРАНЕНЫ ] ---
class DataArchive:
    # Объединенный список ботов (311 + Killer's + начальные)
    BOTS = [
        "@Probivevelocmo_bot", "@pyth1a_0racle_bot", "@visionerobot", "@testFon2vk_bot",
        "@UniversalSearchRobot", "@probei_ru_bot", "@getcontact_real_bot", "@cryptoscanning_bot",
        "@TgAnalyst_bot", "@GetYandexBot", "@GetPhone_Bot", "@LBSE_bot", "@InfoVkUser_bot",
        "@usersbox_bot", "@SEARCHUA_bot", "@ssb_russian_probiv_bot", "@EyeOfAllah_bot",
        "@egrul_bot", "@numberPhoneBot", "@info_baza_bot", "@find_caller_bot"
    ]
    
    # Объединенный список сайтов (305 + 308 + 310 + начальные)
    SITES = [
        "search.carrot2.org", "fboardreader.com", "searchcode.com", "swisscows.com", "intelx.io",
        "yip.su", "archive.is", "phoneradar.ru", "radaris.ru", "afto.lol", "temp-mail.org",
        "publicwww.com", "psbdmp.ws", "kribrum.io", "recon.secapps.com", "aleph.occrp.org", 
        "recruitin.net", "yandex.ru/people", "m.ok.ru/dk?st.cmd=accountRecoverFeedbackForm",
        "my.mail.ru/my/search_people", "tinEye.com", "pimeyes.com", "findclone.ru",
        "mmnt.ru", "spra.vkaru.net", "zytely.rosfirm.info", "fa-fa.kz", "kgd.gov.kz"
    ]

    # Полные тексты мануалов без сокращений
    MANUALS = {
        "full_deanon": (
            "📈 ПЛАН РАСКРЫТИЯ (от Melissa Killer's):\n"
            "1. Потребность -> Мотив -> Построение способов -> Результат.\n"
            "2. Связки для поиска:\n"
            "   • Имя + Город + ДР (число)\n"
            "   • ИФ + Город (отсеивание)\n"
            "   • Родственники: Фамилия + возраст (18+ лет жертвы).\n"
            "   • YouTube ID: поиск в Google для старых названий канала."
        ),
        "parents_pro": (
            "👪 ГЛУБОКИЙ ПОИСК РОДИТЕЛЕЙ (Файл 306):\n"
            "1. OK.ru: Форма восстановления светит часть почты/номера.\n"
            "2. SSB Bot: (@ssb_russian_probiv_bot) — почта/номер для профилей 5+ лет.\n"
            "3. My.Mail.ru: Поиск по Фамилии и Имени -> ссылка с ником -> почта (ник@домен)."
        ),
        "yandex_method": (
            "🔍 МЕТОД 310 (ЯНДЕКС + PHONE):\n"
            "1. yandex.ru/people -> Имя + ДР.\n"
            "2. phoneradar.ru -> Город по номеру.\n"
            "3. В Яндексе ставим фильтр 'Проживание' на этот город. Результат: точный профиль ВК/ОК."
        ),
        "ip_security": (
            "🌐 ЛОГИКА IP И АНОНИМНОСТИ:\n"
            "Любой сайт логирует твой IP. Используй логгеры (iplogger, grabify) для выманивания IP цели. \n"
            "Совет: если не нашел одним способом — рой информацию другим."
        ),
        "swat": "💀 СВАТТИНГ: звонки с легендой и рассылка по @edu.mos.ru."
    }

# --- [ ФУНКЦИОНАЛЬНЫЕ МОДУЛИ ] ---
def search_in_local_db(query):
    results = []
    query = str(query).lower()
    for file in DB_FILES:
        if not os.path.exists(file): continue
        try:
            with open(file, mode='r', encoding='utf-8', errors='ignore') as f:
                delimiter = ';' if 'государственные' in file else ','
                reader = csv.reader(f, delimiter=delimiter)
                for row in reader:
                    if query in " ".join(row).lower():
                        results.append(f"📄 Из файла {file}:\n{', '.join(row)}")
        except: continue
    return results
def ip_intelligence(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"🌐 IP: {ip}\n📍 {r.get('country')}, {r.get('city')}\n📡 Провайдер: {r.get('isp')}"
    except: return "❌ Ошибка IP"

# --- [ ОБРАБОТЧИКИ ТЕЛЕГРАМ ] ---
@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id != ADMIN_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🔍 ЛОКАЛЬНЫЙ ПОИСК", "📱 ПОИСК ПО НОМЕРУ")
    markup.add("🤖 OSINT БОТЫ", "🌐 САЙТЫ / ЛОГГЕРЫ")
    markup.add("👤 МЕТОДЫ & РОДИТЕЛИ", "💀 СВАТТИНГ / ДОКС")
    markup.add("📊 СТАТУС")
    bot.send_message(m.chat.id, "🔱 МОНОЛИТ АКТИВИРОВАН 🔱", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_logic(m):
    if m.from_user.id != ADMIN_ID: return

    if m.text == "🔍 ЛОКАЛЬНЫЙ ПОИСК":
        msg = bot.send_message(m.chat.id, "📝 Введи ФИО, Почту или Номер:")
        bot.register_next_step_handler(msg, process_local)
    elif m.text == "🤖 OSINT БОТЫ":
        bot.send_message(m.chat.id, "🤖 БОТЫ:\n\n" + "\n".join(DataArchive.BOTS))
    elif m.text == "🌐 САЙТЫ / ЛОГГЕРЫ":
        bot.send_message(m.chat.id, "🌐 САЙТЫ:\n\n" + "\n".join(DataArchive.SITES))
    elif m.text == "👤 МЕТОДЫ & РОДИТЕЛИ":
        bot.send_message(m.chat.id, f"{DataArchive.MANUALS['parents_pro']}\n\n{DataArchive.MANUALS['yandex_method']}")
    elif m.text == "💀 СВАТТИНГ / ДОКС":
        bot.send_message(m.chat.id, f"{DataArchive.MANUALS['swat']}\n\n{DataArchive.MANUALS['full_deanon']}")
    elif m.text == "📊 СТАТУС":
        bot.send_message(m.chat.id, f"📂 Файлов: {len(DB_FILES)} | Ботов: {len(DataArchive.BOTS)} | Сайтов: {len(DataArchive.SITES)}")

def process_local(m):
    res = search_in_local_db(m.text)
    for r in res[:10]: bot.send_message(m.chat.id, r)

# --- [ СИСТЕМНЫЙ ЗАПУСК ] ---
def show_lord_banner():
    banner = """
    ███████╗██╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗
    ███████╗██║   ██║██████╔╝█████╗  ██████╔╝
    ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗
    ███████║╚██████╔╝██║     ███████╗██║  ██║
    [ PROJECT ALBERT: THE INFINITE MONOLITH ]
    """
    print(Colorate.Vertical(Colors.red_to_blue, Center.XCenter(banner)))

class HeavyCore: PAYLOAD = "DATA_" * (70 * 1024 * 1024 // 5)

if name == "main":
    show_lord_banner()
    bot.infinity_polling()
# =========================================================
# --- [ БЛОК ИНТЕГРАЦИИ №18: MANUAL_PO_DEANONU ] ---
# =========================================================

class DataArchive_v18:
    # [span_0](start_span)[span_1](start_span)НОВЫЕ БОТЫ ИЗ ФАЙЛА 18[span_0](end_span)[span_1](end_span)
    BOTS_NEW = [
        "@reverseSearch2Bot", "@EyeGodsBot", "@Smart_SearchBot", "@bagosi", 
        "@egrul_bot", "@numberPhoneBot", "@Quick_OSINT_bot", "@clerkinfobot", 
        "@dosie_Bot", "@find_caller_bot", "@get_caller_bot", "@get_kolesa_bot", 
        "@get_kontakt_bot", "@getbank_bot", "@GetFb_bot", "@GetPhone_bot", 
        "@Getphonetestbot", "@info_baza_bot", "@mailsearchbot", "@MyGenisBot", 
        "@phone_avito_bot", "@SafeCallsBot", "@usersbox_bot"
    ]

    # [span_2](start_span)[span_3](start_span)[span_4](start_span)[span_5](start_span)[span_6](start_span)[span_7](start_span)[span_8](start_span)[span_9](start_span)НОВЫЕ САЙТЫ И УТИЛИТЫ[span_2](end_span)[span_3](end_span)[span_4](end_span)[span_5](end_span)[span_6](end_span)[span_7](end_span)[span_8](end_span)[span_9](end_span)
    SITES_NEW = [
        "rulait.github.io/vk-friends-saver", "skyperesolver.net", "vedbex.com/tools/iplogger", 
        "zaprosbaza.pw", "telkniga.com", "reg.ru", "Grabify.link", "Clck.ru", "FTH.SU", 
        "220vk.com", "CheckHost.net", "yzad.ru", "vkdia.com", "searchlikes.ru", "tutnaidut.com",
"flightradar24.com", "vkbarkov.com", "locatefamily.com", "infobel.com", "rocketreach.co", 
        "reestr-zalogov.ru", "kad.arbitr.ru", "sudact.ru", "lampyre.io", "fa-fa.kz", "globfone.com", 
        "mysmsbox.ru", "nuga.app", "spravnik.com", "namechk.com", "rusfinder.pro"
    ]

    # [span_10](start_span)[span_11](start_span)[span_12](start_span)[span_13](start_span)[span_14](start_span)[span_15](start_span)[span_16](start_span)НОВЫЕ ТЕХНИКИ ИЗ МАНУАЛА[span_10](end_span)[span_11](end_span)[span_12](end_span)[span_13](end_span)[span_14](end_span)[span_15](end_span)[span_16](end_span)
    TECHNIQUES = {
        [span_17](start_span)"tele2_win": "⚡️ МЕТОД TELE2: При входе в ЛК на tele2.ru система может выдать инфу о владельце[span_17](end_span).",
        [span_18](start_span)"qiwi_kopilka": "💰 QIWI-КОПИЛКА: Выставляем счет через ссылку копилки, в приложении отобразится номер жертвы[span_18](end_span).",
        "social_eng": "🎭 СОЦ. [span_19](start_span)[span_20](start_span)ИНЖЕНЕРИЯ: Входим в доверие, выманиваем номер через одноклассников (легенда про новый телефон)[span_19](end_span)[span_20](end_span).",
        [span_21](start_span)"card_leak": "💳 ОПЛАТА: При заказе товара номер карты дает ФИО, банк и связь с родителями[span_21](end_span).",
        [span_22](start_span)"stealer": "💾 СТИЛЛЕР: Использование UFR Stealer для кражи паролей из браузеров и софта[span_22](end_span).",
        [span_23](start_span)"ip_logger": "📍 IP-LOGGER: Использование iplogger.ru для маскировки ссылок под обычный контент ВК/Ютуб[span_23](end_span)."
    }

# --- [ ОБРАБОТЧИК ДЛЯ МОДУЛЯ №18 ] ---
@bot.message_handler(func=lambda m: m.text in ["📦 ПАКЕТ №18", "🛡 МЕТОДЫ 18", "🔗 СЕРВИСЫ 18"])
def handle_v18(m):
    if m.from_user.id != ADMIN_ID: return
    
    if m.text == "📦 ПАКЕТ №18":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🛡 МЕТОДЫ 18", "🔗 СЕРВИСЫ 18", "🔙 НАЗАД")
        bot.send_message(m.chat.id, "📁 Данные из Manual_po_deanonu.txt загружены.", reply_markup=markup)
        
    elif m.text == "🛡 МЕТОДЫ 18":
        text = (f"{DataArchive_v18.TECHNIQUES['tele2_win']}\n\n"
                f"{DataArchive_v18.TECHNIQUES['qiwi_kopilka']}\n\n"
                f"{DataArchive_v18.TECHNIQUES['social_eng']}\n\n"
                f"{DataArchive_v18.TECHNIQUES['stealer']}")
        bot.send_message(m.chat.id, text)
        
    elif m.text == "🔗 СЕРВИСЫ 18":
        bots = "\n".join(DataArchive_v18.BOTS_NEW[:15]) # Вывод части для компактности
        sites = "\n".join(DataArchive_v18.SITES_NEW[:15])
        bot.send_message(m.chat.id, f"🤖 НОВЫЕ БОТЫ:\n{bots}\n\n🌐 НОВЫЕ САЙТЫ:\n{sites}")

# --- [ ИНСТРУКЦИЯ ПО ВКЛЕЙКЕ ] ---
# Чтобы кнопка появилась в меню, добавь "📦 ПАКЕТ №18" в основной markup в функции start()
# =========================================================
# =========================================================
# --- [ БЛОК ИНТЕГРАЦИИ: МОДУЛЬ 19 & DESU_PREMIUM ] ---
# =========================================================

class DataArchive_v19:
    # --- [ OSINT БОТЫ: ПОЛНЫЙ СПИСОК ИЗ НОВЫХ ФАЙЛОВ ] ---
    BOTS_ELITE = [
        "@Quick_OSINT_bot", "@clerkinfobot", "@dosie_Bot", "@find_caller_bot",
        "@get_caller_bot", "@get_kolesa_bot", "@get_kontakt_bot", "@getbank_bot",
        "@GetFb_bot", "@GetPhone_bot", "@Getphonetestbot", "@info_baza_bot",
        "@mailsearchbot", "@MyGenisBot", "@phone_avito_bot", "@SafeCallsBot",
        "@usersbox_bot", "@FindNameVk_bot", "@VKUserInfo_bot", "@eyegodszbot",
        "@HowToFind_bot", "@deanonym_bot", "@InstaBot", "@buzzim_alerts_bot",
        "@TempGMailBot", "@VoiceEffectsBot", "@ParserFree2Bot", "@URL2IMGBot"
    ]

    # --- [ ЭКСКЛЮЗИВНЫЕ МЕТОДЫ (DESU & MANUAL) ] ---
    METHODS_PREMIUM = {"yandex_logic": (
            "🛠 ЯНДЕКС-РАЗВЕДКА:\n"
            "1. Берём логин почты -> music.yandex.com/users/ЛОГИН\n"
            "2. В исходном коде ищем 'public_id'.\n"
            "3. Переходим на yandex.ru/user/PUBLIC_ID -> видим все отзывы на картах и маркете."
        ),
        "vk_restore_hack": (
            "🔑 ВК ЧЕРЕЗ ОК:\n"
            "1. Добавляем цель в друзья в ВК.\n"
            "2. В Одноклассниках жмём 'Добавить друзей из ВК'.\n"
            "3. Если нашёлся профиль — идём в ok.ru/password/recovery.\n"
            "4. Вставляем ссылку на профиль ОК -> получаем маскированные почту и номер."
        ),
        "school_find": (
            "🏫 ПОИСК УЧЕБКИ:\n"
            "Фильтруем список друзей цели в ВК по городу. Где больше всего совпадений по одной школе — там он и учится."
        ),
        "ddos_lite": (
            "🔥 DDOS (quezstresser):\n"
            "Target IP: [IP_TARGET], Port: 80, Time: 300s, Method: NTP."
        ),
        "social_eng_phone": (
            "🎭 СИ (ТЕЛЕФОН):\n"
            "Пишем однокласснику: 'Привет, дай номер [Имя_Цели], а то у меня трубка новая, контакты слетели'. Работает в 80% случаев."
        )
    }

    # --- [ ТЕХНИЧЕСКИЙ ИНСТРУМЕНТАРИЙ ] ---
    TOOLS_SITES = [
        "telkniga.com", "iplogger.ru", "220vk.com", "findclone.ru", "search4faces.com",
        "vk.watch", "rusfinder.pro", "clck.ru", "grabify.link", "lampyre.io", "fa-fa.kz",
        "kad.arbitr.ru", "reestr-zalogov.ru", "iknowwhatyoudownload.com"
    ]

# --- [ ОБРАБОТЧИК ДЛЯ НОВОГО МОДУЛЯ ] ---
@bot.message_handler(func=lambda m: m.text in ["🔱 МОНОЛИТ v19", "🧪 МЕТОДЫ DESU", "📱 OSINT v19"])
def handle_v19_logic(m):
    if m.from_user.id != ADMIN_ID: return
    
    if m.text == "🔱 МОНОЛИТ v19":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("🧪 МЕТОДЫ DESU", "📱 OSINT v19", "🔙 НАЗАД")
        bot.send_message(m.chat.id, "⚡️ Синхронизация с 19-м файлом и мануалом Desu завершена.", reply_markup=markup)

    elif m.text == "🧪 МЕТОДЫ DESU":
        text = (f"{DataArchive_v19.METHODS_PREMIUM['yandex_logic']}\n\n"
                f"{DataArchive_v19.METHODS_PREMIUM['vk_restore_hack']}\n\n"
                f"{DataArchive_v19.METHODS_PREMIUM['ddos_lite']}")
        bot.send_message(m.chat.id, text)

    elif m.text == "📱 OSINT v19":
        bots = "\n".join(DataArchive_v19.BOTS_ELITE[:15])
        sites = "\n".join(DataArchive_v19.TOOLS_SITES)
        bot.send_message(m.chat.id, f"📡 ОБНОВЛЕННЫЙ АРСЕНАЛ:\n\nБОТЫ:\n{bots}\n\nСЕРВИСЫ:\n{sites}")

# --- [ СИСТЕМНОЕ УВЕДОМЛЕНИЕ ] ---
# Добавь кнопку "🔱 МОНОЛИТ v19" в своё главное меню (start).
# =========================================================
# =========================================================
# --- [ БЛОК ИНТЕГРАЦИИ №20: OSINT BY @HESONBY ] ---
# =========================================================

class DataArchive_v20:
    # --- [ ДОРКИ И СПЕЦ-ЗАПРОСЫ ] ---
    DORK_PATTERNS = {
        "google_file": "filetype:pdf [Запрос] — поиск документов (паспорта, списки, приказы).",
        "site_search": "site:gov.ru [Запрос] — поиск только по гос-ресурсам.",
        "intext_search": "intext:\"confidential\" — поиск страниц с конфиденциальной инфой.",
        "yandex_personal": "site:vk.com \"[Имя]\" — точный поиск человека в конкретной соцсети."
    }

    # --- [ АНАЛИТИКА И ФАКТЧЕКИНГ ] ---
    PROFESSIONAL_TIPS = {
        "photo_bg": "🖼 АНАЛИЗ ФОНА: Ищи логотипы на машинах (доставка), названия ЖК, номера регионов на авто.",
        "metadata": "💾 META-DATA: Используй софт для проверки EXIF (дата, время, модель камеры, GPS-координаты).",
        "whois": "🌐 WHOIS: Проверяй владельца домена через WhoIs. Регистратор != Хостинг.",
        "factcheck": "⚖️ ПРИНЦИП: Минимум 3 независимых источника для подтверждения одной зацепки."
    } # --- [ ОФИЦИАЛЬНЫЕ ИСТОЧНИКИ ] ---
    GOV_SOURCES = [
        "fssp.gov.ru — база долгов и исполнительных производств.",
        "gibdd.ru/check — проверка штрафов и владельцев авто.",
        "egrul.nalog.ru — данные по ИП и Юрлицам.",
        "service.nalog.ru/inn.html — поиск ИНН по паспортным данным."
    ]

# --- [ ОБРАБОТЧИК ДЛЯ МОДУЛЯ №20 ] ---
@bot.message_handler(func=lambda m: m.text in ["🎓 КУРС @HESONBY", "🔍 ДОРКИ & GOV", "🧠 АНАЛИЗ ФОНА"])
def handle_v20_logic(m):
    if m.from_user.id != ADMIN_ID: return
    
    if m.text == "🎓 КУРС @HESONBY":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("🔍 ДОРКИ & GOV", "🧠 АНАЛИЗ ФОНА", "🔙 НАЗАД")
        bot.send_message(m.chat.id, "🎓 Обучение OSINT от @hesonby интегрировано.\nПереход в режим профессиональной аналитики.", reply_markup=markup)

    elif m.text == "🔍 ДОРКИ & GOV":
        dorks = "\n\n".join(DataArchive_v20.DORK_PATTERNS.values())
        gov = "\n".join(DataArchive_v20.GOV_SOURCES)
        bot.send_message(m.chat.id, f"📡 ДОРКИ ДЛЯ ПОИСКА:\n\n{dorks}\n\n🏛 ГОС-ИСТОЧНИКИ:\n{gov}")

    elif m.text == "🧠 АНАЛИЗ ФОНА":
        tips = (f"{DataArchive_v20.PROFESSIONAL_TIPS['photo_bg']}\n\n"
                f"{DataArchive_v20.PROFESSIONAL_TIPS['metadata']}\n\n"
                f"{DataArchive_v20.PROFESSIONAL_TIPS['factcheck']}")
        bot.send_message(m.chat.id, f"👁 ГЛАЗ ПРОФЕССИОНАЛА:\n\n{tips}")

# --- [ ИНСТРУКЦИЯ ] ---
# Просто добавь "🎓 КУРС @HESONBY" в меню старта. 
# =========================================================
# =========================================================
# --- [ БЛОК ИНТЕГРАЦИИ №21: SOCMINT & СНОС ОТ @FUCKCWEX ] ---
# =========================================================

class DataArchive_v21:
    # --- [ СПЕЦ-БОТЫ ДЛЯ ТЕЛЕГРАМ-РАЗВЕДКИ ] ---
    PROBIV_BOTS = [
        "@cwexprobiv_robot",  # Главный бот по версии fuckcwex (номер по ID)
        "@vektor_info99_bot", # Поиск по ФИО, почте, IP и картам
        "@breakruinrobot",    # Бот для массовых жалоб (снос аккаунтов)
        "@Quick_OSINT_bot"    # Дополнительный пробив по базам
    ]

    # --- [ SOCMINT ИНСТРУМЕНТЫ ] ---
    SOCMINT_TOOLS = [
        "checkusernames.com — проверка доступности ника",
        "namechk.com — поиск ника по сотням ресурсов",
        "rusfinder.pro — глубокий поиск в RU-сегменте"
    ]

    # --- [ ТЕХНИКИ СНОСА И АНАЛИЗА ] ---
    TECHNIQUES_V21 = {
        "tag_analysis": (
            "🏷 АНАЛИЗ ТЕГОВ:\n"
            "Если в GetContact цель записана как 'Ангелина 10Б' — ты сразу получил Имя, Пол и место учебы (класс)."
        ),
        "tg_delete": (
            "📉 СНОС АККАУНТА (REPORTING):\n"
            "Снос происходит через массовые жалобы. Используются ботнеты (типа @breakruinrobot) или софты, "
            "рассылающие 10.000+ жалоб на почту поддержки Telegram. Работает лучше всего на новорегах."
        ),
        "social_logic": (
            "🧩 ПРАВИЛО ЦЕПОЧКИ:\n"
            "Номер -> Теги -> ФИО -> Соцсети -> Друзья -> Школа/Работа. Эффективность зависит от умения сопоставлять данные."
        )
    }

# --- [ ОБРАБОТЧИК ДЛЯ МОДУЛЯ №21 ] ---
@bot.message_handler(func=lambda m: m.text in ["🛡 ОБУЧЕНИЕ @FUCKCWEX", "🧨 СНОС & ЖАЛОБЫ", "📊 SOCMINT АРСЕНАЛ"])
def handle_v21_logic(m):
    if m.from_user.id != ADMIN_ID: return
    
    if m.text == "🛡 ОБУЧЕНИЕ @FUCKCWEX":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("🧨 СНОС & ЖАЛОБЫ", "📊 SOCMINT АРСЕНАЛ", "🔙 НАЗАД")
        bot.send_message(m.chat.id, "🛡 Обучение SOCMINT от @fuckcwex интегрировано.\nГотов к операциям по сносу и глубокой разведке.", reply_markup=markup)

    elif m.text == "🧨 СНОС & ЖАЛОБЫ":
        bot.send_message(m.chat.id, f"🧨 МЕТОДИКА СНОСА:\n\n{DataArchive_v21.TECHNIQUES_V21['tg_delete']}\n\n🤖 Рекомендуемый бот: @breakruinrobot")
elif m.text == "📊 SOCMINT АРСЕНАЛ":
        bots = "\n".join(DataArchive_v21.PROBIV_BOTS)
        tools = "\n".join(DataArchive_v21.SOCMINT_TOOLS)
        analysis = DataArchive_v21.TECHNIQUES_V21['tag_analysis']
        bot.send_message(m.chat.id, f"📡 ИНСТРУМЕНТЫ РАЗВЕДКИ:\n\nБОТЫ:\n{bots}\n\nСЕРВИСЫ:\n{tools}\n\nСОВЕТ:\n{analysis}")

# --- [ СИСТЕМНАЯ ЗАМЕТКА ] ---
# Добавь кнопку "🛡 ОБУЧЕНИЕ @FUCKCWEX" в стартовое меню. 
# =========================================================
# =========================================================
# --- [ БЛОК ИНТЕГРАЦИИ №22: АВТО-СНОСЕР (RAKUZAN LOGIC) ] ---
# =========================================================

class SnoserModule_v22:
    # База SMTP-аккаунтов (добавляй сюда свои почты для мощности)
    SENDERS = {
        'sanya.dragonov@mail.ru': 'RakuzanSnos',
        'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
        'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ'
    }
    
    RECEIVERS = ['support@telegram.org', 'abuse@telegram.org']

    # Шаблоны из snos.py (самые эффективные)
    TEMPLATES = {
        "account": "Hello support! On your platform, I found a user who violates the rules and distributes illegal content. Please block this user. Target: {target}",
        "channel": "Hello, dear telegram support. On your platform, I found a channel that distributes prohibited content. Here is the link: {target}. Please take action.",
        "bot": "Hello, telegram support. I found a bot that searches for personal data of users. Link: {target}. Please block it."
    }

    @staticmethod
    def fire_reports(target, mode="account"):
        """Автоматическая рассылка жалоб по списку почт"""
        report_text = SnoserModule_v22.TEMPLATES.get(mode, "account").format(target=target)
        sent_count = 0
        
        for email, password in SnoserModule_v22.SENDERS.items():
            try:
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = random.choice(SnoserModule_v22.RECEIVERS)
                msg['Subject'] = f"Report {mode.upper()}"
                msg.attach(MIMEText(report_text, 'plain'))

                # Настройка для Mail.ru (как в snos.py)
                server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
                server.login(email, password)
                server.sendmail(email, msg['To'], msg.as_string())
                server.quit()
                sent_count += 1
                time.sleep(2) # Задержка между атаками
            except Exception as e:
                print(f"Ошибка на {email}: {e}")
        return sent_count

# --- [ ОБРАБОТЧИК БОЕВОГО ИНТЕРФЕЙСА ] ---
@bot.message_handler(func=lambda m: m.text in ["💀 СНОСИТЕЛЬ", "🧨 АТАКА НА АКК", "📢 СНОС КАНАЛА", "🤖 СНОС БОТА"])
def handle_snos_v22(m):
    if m.from_user.id != ADMIN_ID: return

    if m.text == "💀 СНОСИТЕЛЬ":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("🧨 АТАКА НА АКК", "📢 СНОС КАНАЛА", "🤖 СНОС БОТА", "🔙 НАЗАД")
        bot.send_message(m.chat.id, "🛰 СИСТЕМА СНОСА АКТИВИРОВАНА\nВыбери тип цели:", reply_markup=markup)

    elif m.text in ["🧨 АТАКА НА АКК", "📢 СНОС КАНАЛА", "🤖 СНОС БОТА"]:
        mode_map = {"🧨 АТАКА НА АКК": "account", "📢 СНОС КАНАЛА": "channel", "🤖 СНОС БОТА": "bot"}
        mode = mode_map[m.text]
        msg = bot.send_message(m.chat.id, f"Введите юзернейм или ссылку на {mode}:")
        bot.register_next_step_handler(msg, lambda message: execute_attack(message, mode))

def execute_attack(m, mode):
    target = m.text
    bot.send_message(m.chat.id, f"🚀 АТАКА НАЧАТА!\nЦель: {target}\nИспользую базу почт...")
    
    count = SnoserModule_v22.fire_reports(target, mode)
    
    if count > 0:
        bot.send_message(m.chat.id, f"🔥 ОПЕРАЦИЯ ЗАВЕРШЕНА!\nУспешно отправлено {count} жалоб с разных почт.")
    else:
        bot.send_message(m.chat.id, "❌ ОШИБКА АТАКИ!\nНи одна почта не сработала. Проверь пароли в коде.")
# --- [ ИНСТРУКЦИЯ ] ---
# Просто добавь кнопку "💀 СНОСИТЕЛЬ" в главное меню start.
# =========================================================
# =========================================================
# --- [ БЛОК ИНТЕГРАЦИИ: FRAMEWORK v1.0 & LOCAL DB ] ---
# =========================================================

import csv
import os

class FrameworkModule_v23:
    # Пути к твоим файлам (убедись, что они лежат в одной папке со скриптом)
    BASE_FILES = [
        'билайн юзеры.csv',
        'государственные услуги p1.csv',
        'государственные услуги p2.csv',
        'государственные услуги p3.csv'
    ]

    @staticmethod
    def search_in_local_db(query):
        """Поиск по всем загруженным CSV базам"""
        results = []
        query = query.lower()
        
        for file_name in FrameworkModule_v23.BASE_FILES:
            if not os.path.exists(file_name):
                continue
                
            try:
                # Определяем разделитель (в госуслугах он ';', в билайне ',')
                delimiter = ';' if 'государственные' in file_name else ','
                
                with open(file_name, mode='r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f, delimiter=delimiter)
                    for row in reader:
                        row_str = " ".join(row).lower()
                        if query in row_str:
                            results.append(f"📂 [{file_name}]: {' | '.join(row)}")
                        if len(results) >= 10: break # Ограничение выдачи
            except Exception as e:
                print(f"Ошибка чтения {file_name}: {e}")
                
        return results

# --- [ ОБРАБОТЧИК ДЛЯ FRAMEWORK ] ---
@bot.message_handler(func=lambda m: m.text in ["🔍 ЛОКАЛЬНЫЙ ПОИСК", "📂 БАЗЫ ДАННЫХ"])
def handle_framework_v23(m):
    if m.from_user.id != ADMIN_ID: return

    if m.text == "📂 БАЗЫ ДАННЫХ":
        status = ""
        for f in FrameworkModule_v23.BASE_FILES:
            exists = "✅" if os.path.exists(f) else "❌"
            status += f"{exists} {f}\n"
        bot.send_message(m.chat.id, f"📊 СТАТУС ЛОКАЛЬНЫХ БАЗ:\n\n{status}")

    elif m.text == "🔍 ЛОКАЛЬНЫЙ ПОИСК":
        msg = bot.send_message(m.chat.id, "Введите запрос для поиска (ФИО, Номер или Почту):")
        bot.register_next_step_handler(msg, execute_local_search)

def execute_local_search(m):
    query = m.text
    bot.send_message(m.chat.id, f"🔎 Ищу '{query}' в локальных базах...")
    
    results = FrameworkModule_v23.search_in_local_db(query)
    
    if results:
        full_text = "🎯 НАЙДЕНЫ СОВПАДЕНИЯ:\n\n" + "\n\n".join(results)
        if len(full_text) > 4096:
            full_text = full_text[:4000] + "\n\n... (данные обрезаны)"
        bot.send_message(m.chat.id, full_text)
    else:
        bot.send_message(m.chat.id, "🤷‍♂️ Ничего не найдено в локальных CSV.")

# --- [ СИСТЕМНАЯ УСТАНОВКА ] ---
# Добавь кнопки "🔍 ЛОКАЛЬНЫЙ ПОИСК" и "📂 БАЗЫ ДАННЫХ" в главное меню.
# =========================================================
# =========================================================
# ДОПОЛНИТЕЛЬНЫЙ МОДУЛЬ: ДАННЫЕ ИЗ ОБУЧЕНИЯ @USERCWEX
# =========================================================

def get_usercwex_data():
    """
    Возвращает структурированные данные из мануала @usercwex:
    боты, сервисы визуализации и методы.
    """
    data = {
        "probiv_bots": [
            "@hhjvgghv_bot", 
            "@VEKTOR_AwleV_Robot", 
            "@bestttosintbot", 
            "@cwexprobiv_robot", 
            "@vektor_info99_bot"
        ],
        "visualization": [
            "lucid.co", 
            "napkin.ai"
        ],
        "osint_resources": [
            "osintframework.com", 
            "osintkit.net", 
            "tryhackme.com/r/room/sakura"
        ],
        "snos_info": (
            "Снос аккаунта: массовые жалобы через ботнеты (напр. @breakruinrobot) "
            "или софты, отправляющие жалобы на почту (нужно ~10.000 почт)."
        )
    }
    return data
def show_cwex_manual():
    """
    Возвращает текстовую выжимку мануала для вывода в консоль или боту.
    """
    info = get_usercwex_data()
    output = "🚀 РЕСУРСЫ ИЗ ОБУЧЕНИЯ @USERCWEX:\n\n"
    output += "🤖 БОТЫ: " + ", ".join(info["probiv_bots"]) + "\n"
    output += "📊 ВИЗУАЛИЗАЦИЯ: " + ", ".join(info["visualization"]) + "\n"
    output += "🌐 OSINT САЙТЫ: " + ", ".join(info["osint_resources"]) + "\n\n"
    output += f"💀 МЕТОД СНОСА: {info['snos_info']}"
    return output

# =========================================================
# =========================================================
# МОДУЛЬ ИЗ ОБУЧЕНИЯ @USERCWEX (ДОБАВИТЬ В КОНЕЦ ФАЙЛА)
# =========================================================

def get_cwex_intelligence_data():
    """
    Возвращает полную базу инструментов и методов из обучения @usercwex
    """
    cwex_database = {
        "bots": {
            "main": ["@cwexprobiv_robot", "@vektor_info99_bot"],
            "additional": ["@hhjvgghv_bot", "@VEKTOR_AwleV_Robot", "@bestttosintbot", "@vektor_info99_bot"]
        },
        "resources": {
            "search": ["osintframework.com", "osintkit.net", "hunter.io", "haveibeenpwned.com"],
            "visualization": ["lucid.co", "napkin.ai"],
            "practice": ["tryhackme.com/r/room/sakura"]
        },
        "methods": {
            "snos": "Массовые жалобы через ботнеты (напр. @breakruinrobot) или SMTP-софты (требуется ~10.000 почт).",
            "anon": ["Tor Browser", "VPN (без логов)", "SOCKS5 прокси", "Анонимные почты (temp-mail)"]
        }
    }
    return cwex_database

def cwex_manual_brief():
    """
    Генерирует текстовый отчет по методам из файла обучения
    """
    db = get_cwex_intelligence_data()
    report = (
        "🔱 ИНСТРУМЕНТАРИЙ @USERCWEX 🔱\n\n"
        f"🤖 БОТЫ ПРОБИВА: {', '.join(db['bots']['main'])}\n"
        f"🔎 ДОП. РОБОТЫ: {', '.join(db['bots']['additional'])}\n"
        f"📊 АНАЛИТИКА: {', '.join(db['resources']['visualization'])}\n"
        f"🌐 OSINT БАЗЫ: {', '.join(db['resources']['search'])}\n\n"
        f"💀 МЕТОД СНОСА: {db['methods']['snos']}\n"
        f"🛡️ АНОНИМНОСТЬ: {', '.join(db['methods']['anon'])}"
    )
    return report

# Пример вызова: print(cwex_manual_brief())
# =========================================================
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os

# Пытаемся импортировать библиотеки для оформления
try:
    from colored import cprint
    from pystyle import Colors, Colorate
except ImportError:
    def cprint(text, color=None): print(text)
    class Colorate:
        @staticmethod
        def Horizontal(color, text): return text
    class Colors:
        blue_to_red = None

# =========================================================
# БЛОК 1: БАЗА ПОЧТ (SENDERS)
# =========================================================
senders = {
    'qstkennethadams388@gmail.com':'itpz jkrh mtwp escx',
    'usppaullewis171@gmail.com':'lpiy xqwi apmc xzmv',
    'ftkgeorgeanderson367@gmail.com':'okut ecjk hstl nucy',
    'nieedwardbrown533@gmail.com':'wvig utku ovjk appd',
    'h56400139@gmail.com':'byrl egno xguy ksvf',
    'den.kotelnikov220@gmail.com':'xprw tftm lldy ranp',
    'trevorzxasuniga214@gmail.com':'egnr eucw jvxg jatq',
    'dellapreston50@gmail.com':'qoit huon rzsd eewo',
    'neilfdhioley765@gmail.com':'rgco uwiy qrdc gvqh',
    'hhzcharlesbaker201@gmail.com':'mcxq vzgm quxy smhh',
    'samuelmnjassey32@gmail.com':'lgct cjiw nufr zxjg',
    'allisonikse1922@gmail.com':'tozo xrzu qndn mwuq',
    'corysnja1996@gmail.com':'pfjk ocbf augx cgiy',
    'maddietrdk1999@gmail.com':'rhqb ssiz csar cvot',
    'yaitskaya.alya@mail.ru':'CeiYHA6GNpvuCz584eCp',
    'yelena.polikarpova.1987@mail.ru':'70Ktuvrs1iYbvSnbK8hG',
    'yeva.zuyeva.85@mail.ru':'EBjgRqq73hue9dGhUA2R',
    'zina.yagovenko.69@mail.ru':'QKBmpXnzFZVu9w4ewSrA',
    'ilya.yaroslavov.72@mail.ru':'A2gNkb8n54i4T7XdPdH5',
    'maryamna.moskvina.62@mail.ru':'dT7ftdX72cMsVemqRRqu',
    'zina.zhvikova@mail.ru':'7CwRkjeL3a5viE9we3bt',
    'boyarinova.fisa@mail.ru':'NnJfmSBzQ9Eew09xirpY',
    'prokhor.sveshnikov.73@mail.ru':'Ybunrxdf95gkzm6A6ipp',
    'azhikelyamov.yulian@mail.ru':'r7hanfr0tMqcBE4Edmg0',
    'prokhor.siyantsev@mail.ru':'yubs6kvtfpWT4Tram26e',
    'yablonev90@mail.ru':'42krThdaYbWCrCbH8UgK',
    'mari.dvornikova.86@mail.ru':'qdEzYLWSTz6UEM2E4i0u',
    'vika.tobolenko.96@mail.ru':'3WQ2wFTwge9m2C09QsfK',
    'koporikov.yura@mail.ru':'nJtyfjqYi91j7tk0udNx',
    'zina.podshivalova.92@mail.ru':'u4CL3YxVutmiuTvmTrbu',
    'leha.novitskiy.71@mail.ru':'qQZd1gMqkU906Xk2hgJJ',
    'polina.karaseva.1987@mail.ru':'mxZUqPPTrZHK99jUfPhB',
    'prokhor.sablin.82@mail.ru':'vN7FjmmCmAD0JnQsANyc',
    'kade.kostya@mail.ru':'U0hdXu7y3c1AVeT1Vpn9',
    'yelizaveta.novokshonova.71@mail.ru':'aKPpgaPDuwaKbX1pbcq3',
    'pozdovp@mail.ru':'EGDd20c7s82Z0s9LmrXc',
    'siyasinovy@mail.ru':'z2ZdsRL04JvBYZrrjrvv',
    'nina.gref.73@mail.ru':'sitw1XTxCVgji061iqj7',
    'fil.golubkin.80@mail.ru':'PeaLrzjbn408DEeiqmQq',
    'venedikt.babinov.71@mail.ru':'tBewA1HQm29c2Zkira96',
    'den.verderevskiy.67@mail.ru':'fndp7qr67dpfXBAu0ePH',
    'olga.viranovskaya.92@mail.ru':'50QSPrecgk5cMdk1YsBm',
    'uyankilovich@mail.ru':'Muw9kX9vAhhKxbZXZ3sh',
    'clqdxtqbfj@rambler.ru':'8278384a3L51C',
    'qeuvkzwxao@rambler.ru':'72325556pMFol',
    'mgiwwgbjqt@rambler.ru':'3180204jCoAdt',
    'olwogjcicw@rambler.ru':'3993480P4Gyth',
    'qjdmjszsnc@rambler.ru':'6545403StkbOh',
    'yqoibpcoki@rambler.ru':'695328653f9Wp',
    'vnlhjjkbxr@rambler.ru':'4609313egqV59',
    'vpgcdkunar@rambler.ru':'9936120R4LYh3',
    'agycsnogqq@rambler.ru':'0234025nWwX5j',
    'ctmhzsngse@rambler.ru':'2480571s1sZvW',
    'ryztzlttdn@rambler.ru':'9416368kTX5jI',
    'hqxybovebw@rambler.ru':'8245145VhX704',
    'rejrjswkwb@rambler.ru':'5114881xCYqsB',
    'xkbecjvxnx@rambler.ru':'5670524FiFi39',
    'xnlqkfvwzx@rambler.ru':'7911186rp8L9P',
    'gvzzmqtuzy@rambler.ru':'5133370ZstXEx',
    'eijxsbjyfy@rambler.ru':'36196124YQZeI',
    'bizdlfuahq@rambler.ru':'8374903tkk2gA',
    'dhehumtsef@rambler.ru':'9126453AkhK0Z',
    'zsotxpaxvi@rambler.ru':'46227528QryxI',
    'ktsgdygeuc@rambler.ru':'1853586bnCyzK',
    'uiacgqvgpe@rambler.ru':'65280104FvoJW',
    'ynazuhytyd@rambler.ru':'1038469bD3PXc',
    'ewmyymarvi@rambler.ru':'5023318Bh3tBg',
    'wllhpdisuj@rambler.ru':'24856958LdTsS',
    'ldqicaqxqo@rambler.ru':'3878601ZNDUtq',
    'qnuumqoreq@rambler.ru':'97575207Is6tx',
    'hlqhvdwpvn@rambler.ru':'6886684bPjiyd',
    'mjjjxiuadq@rambler.ru':'0606032V81m1F',
    'qmasujqfrk@rambler.ru':'277585511anUy',
    'mfemvxqdcq@rambler.ru':'8831015UwqwWD',
    'jauvxszfam@rambler.ru':'0711044gqzrVR',
    'lkmujuagfk@rambler.ru':'08781007DLS8k',
    'kcamwmzxjo@rambler.ru':'9812873rVr1MY',
    'czkklwifon@rambler.ru':'74278883h9FP8',
    'tsjsbqyrfk@rambler.ru':'0150917jIseH2',
    'pbetvcnhzh@rambler.ru':'9952234XaKDFu',
    'bsahxcpwkw@rambler.ru':'2860163ch8Ido',
    'xphyesgbtc@rambler.ru':'6594341ERehhX',
    'egmpjoufeq@rambler.ru':'2613441hfDuWr',
    'jyaolatwam@rambler.ru':'7668835xdjLbg',
    'istooplcmf@rambler.ru':'6592403JR47Wm',
    'vxesoednot@rambler.ru':'35885918QZw94',
    'oywtklayaz@rambler.ru':'4434448KsCuTf',
    'tazxrlpjil@rambler.ru':'8342862p9Wyst',
    'aumiycpxid@rambler.ru':'4109383BuuNcN',
    'lrrztbfuzy@rambler.ru':'3646406sDO8ay',
    'ocggavguxr@rambler.ru':'6406050SL2mZG',
    'imprdsrnmd@rambler.ru':'4869746vpxksJ',
    'eidyoikavp@rambler.ru':'1243890yXPyix',
    'jtbcabsapw@rambler.ru':'566339497yHv3',
    'szokdvnzrw@rambler.ru':'5285567I3Bil1',
    'jqflrccfjs@rambler.ru':'7239478VeLuf1',
    'nhmxjawemh@rambler.ru':'22695409fkCex',
    'uoolwvvwdc@rambler.ru':'1073090zX6ebM',
    'bdnptczren@rambler.ru':'2684430DcPEuk',
    'bfghzdkurg@rambler.ru':'3874335d5hDQy',
    'ljlexsfcvo@rambler.ru':'4102671EIquGo',
    'byzjhysyyg@rambler.ru':'4637736mzdEcT',
    'tlrjbuzcyj@rambler.ru':'2437827AhPaGW',
    'denjsbmggh@rambler.ru':'228014585ayVe',
    'ekkjrcskzo@rambler.ru':'6609442MFPeDO',
    'ptpjocqobw@rambler.ru':'6047270EXk7Hb',
    'nekrxmcklm@rambler.ru':'3532718I3vV4C',
    'ulgqeqvdqy@rambler.ru':'6764301Nx25yL',
    'ezofozvhyn@rambler.ru':'43181265tC6FQ',
    'hwklsnkqky@rambler.ru':'2399374mHyEUJ',
    'elglaqexoj@rambler.ru':'9803014pMNF9p',
    'rgmjfwhhjs@rambler.ru':'3268611cfC3aR',
    'vcvwvkntgb@rambler.ru':'6536007UgTXg4',
    'phkohtlitv@rambler.ru':'0238010TXt5aN',
    'pqqqyejlqi@rambler.ru':'0429804UwSSi2',
    'toxevermnd@rambler.ru':'1801000MqDm87',
    'dicfdqgxad@rambler.ru':'2062460Tbvjlz',
    'sktsnxhcxe@rambler.ru':'35185285Pon91',
    'jpljjnrrla@rambler.ru':'0815671xPHjiw',
    'rtqpiimiid@rambler.ru':'6534672URa1mI',
    'ldygdlpizk@rambler.ru':'6686886YWhL05',
    'fqxqadaxfy@rambler.ru':'3195621x5qYdU',
    'chybzpsglw@rambler.ru':'8032931YTKllg',
    'vkctzanare@rambler.ru':'1157997LGySqk',
    'repjncygun@rambler.ru':'3300691BqYJVG',
    'khrarivdow@rambler.ru':'7168350Cmqkmj',
    'aqbeitoqdl@rambler.ru':'87552792499tS',
    'vhauhgmbnc@rambler.ru':'9276444y9YzY1',
    'cfoqabqkbi@rambler.ru':'4601718gc2Zji',
    'kmqnowhvjp@rambler.ru':'6667003L1jZxc',
    'djsdksvzhj@rambler.ru':'7523251yAKPjZ',
    'uztbbbfqbp@rambler.ru':'8265517naN9fx',
    'ljrbpfuicp@rambler.ru':'39793362TjZIk',
    'jzzdyxicjo@rambler.ru':'8117494s6CZVB',
    'gjnbtrflkc@rambler.ru':'8623171iqXOD9',
    'jfjtwncyeb@rambler.ru':'7066987lMSG2Z',
    'rfphqkyyrj@rambler.ru':'8800207M5Nj7Y',
    'ilynipkqwx@rambler.ru':'83333032WQo83',
    'ifzenleixs@rambler.ru':'69679436xM9U4',
    'oevwtysoel@rambler.ru':'6918228UC47Zs',
    'hpdkdwqvzx@rambler.ru':'0605431xMVexd',
    'ekbkufxdxx@rambler.ru':'1918712uEOQ9t',
    'zstxwfwiof@rambler.ru':'4043772UwRp5o',
    'rjmrbybhnd@rambler.ru':'5203792lDmxvC',
    'eukygnfzno@rambler.ru':'3520959hXs1Zw',
    'ljrolbwlad@rambler.ru':'0394475pK0dYa',
    'gozpezocmj@rambler.ru':'8282635Gkvuvq',
    'asytoiumwt@rambler.ru':'42141199FgP3H',
    'fbiooohghv@rambler.ru':'7338453zMbWhb',
    'ajwlalfqqu@rambler.ru':'3360915x1XVgt',
    'cvegntetwm@rambler.ru':'8091607CSuKMf',
    'jnhjnmicbt@rambler.ru':'6375986dokrgG',
    'fnaauasmjz@rambler.ru':'4160248ztCRsJ',
    'qnwmlvfwct@rambler.ru':'8367630XGXmxW',
    'lkycbhjcwp@rambler.ru':'5255980KedZTc',
    'bkyojwrkxl@rambler.ru':'1286663uHl4WQ',
    'lxddybklck@rambler.ru':'1077242JFSyQN',
    'chzhdkoxnp@rambler.ru':'0533445SI0q7c',
    'ofjxkwwomf@rambler.ru':'04956317DKrSX',
    'jlirgtapbl@rambler.ru':'8728917NdMxgN',
    'dgcceghlse@rambler.ru':'2986381aT5V36',
    'rkwfhcvlem@rambler.ru':'10022063K5qmY',
    'orgjvhbrxw@rambler.ru':'0652659TopL8Z',
    'opynskpmzp@rambler.ru':'2881423L4qs6x',
    'pbqzrueeko@rambler.ru':'44469262tOGeK',
    'raxzhngqti@rambler.ru':'3078265mgWYjl',
    'ztnxozwuuj@rambler.ru':'0637919utKekj',
    'gtxjzwlgio@rambler.ru':'3737088WWddrY',
    'sjbflcwjgn@rambler.ru':'9791667kVGllD',
    'znggdpfxzu@rambler.ru':'0209083jdisUI',
    'gnvhlocnro@rambler.ru':'4361239Vu3OCl',
    'vqeijhgrmo@rambler.ru':'5560137M1oKk2',
    'meefvzfwqb@rambler.ru':'9793015vJE0qF',
    'sclsjzvugn@rambler.ru':'4631432OQjvWt',
    'ybbtiosefy@rambler.ru':'3511505pL04S1',
    'agwqdadpkb@rambler.ru':'0930298CUZdLp',
    'kudgvibwao@rambler.ru':'5791834nlLQtU',
    'qyonxjqbxi@rambler.ru':'9390829m2Edz3',
    'jhetdlhlqk@rambler.ru':'5530162MiLHZe',
    'bsjvczarsc@rambler.ru':'5747155KvNjcL',
    'wlcilpvzqu@rambler.ru':'2757580jLlM9M',
    'xxdgcixidw@rambler.ru':'2867562O7zGft',
    'wekduwrnkp@rambler.ru':'2646367TlIskI',
    'keakcnrorg@rambler.ru':'9223165cV1Jj8',
    'nzuspyevwr@rambler.ru':'2212416npkUqe',
    'mgjfbgitts@rambler.ru':'7368986roeLXD',
    'smfxvrnhmu@rambler.ru':'6947298Kau5qA',
    'yvkelubdzf@rambler.ru':'5913332lXWtlC',
    'bwywtjxybd@rambler.ru':'2766021wTSkeU',
    'dlvyzavolw@rambler.ru':'274983252lHyu',
    'oaudcugulf@rambler.ru':'4543030UHFWaV',
    'zvqexaokhf@rambler.ru':'1453114PCheCq',
    'pjuafpzpoo@rambler.ru':'8474216vNFUG0',
    'ckryhpqogh@rambler.ru':'4791674aJHW43',
    'vlkqstbhpd@rambler.ru':'3021260kBI3KU',
    'jwuupemjpm@rambler.ru':'7769235y719L9',
    'bmxuqrzcnk@rambler.ru':'1345552ExHXyu',
    'fqrkonqkjc@rambler.ru':'4104158bVEORa',
    'gizwbhyrfd@rambler.ru':'3863359lgfpTv',
    'onghqwbvnz@rambler.ru':'8249537XWqpPk',
    'aeyeyvlnkl@rambler.ru':'6025219f5mGom',
    'qcwweqcqbx@rambler.ru':'2503306kHzKPD',
    'vefmynztzu@rambler.ru':'1134939bhRpJS',
    'qlkhitdctp@rambler.ru':'31621358ZPx5F',
    'xhgfgecvrn@rambler.ru':'4116759TRhERi',
    'globizrzui@rambler.ru':'9679753mLkmMd',
    'vvfcuoibrf@rambler.ru':'13558992CDkJj',
    'enccmwktap@rambler.ru':'7631476Lzr9hd',
    'njbnyghvdq@rambler.ru':'48585907Qh2NS',
    'cobadewaxd@rambler.ru':'6433228NMX7a0',
    'zzvsuoiqfx@rambler.ru':'5067380KtnMTb',
    'lkdcjpcqxu@rambler.ru':'8319085aRHdoT',
    'zcabeofgox@rambler.ru':'0059181TJSaJq',
    'rswrifhmtf@rambler.ru':'2987108xzf1Uy',
    'gebzgyscic@rambler.ru':'6981082UOD1sL',
    'yhncgfwjom@rambler.ru':'7866073mRMAal',
    'pvvlmjmiwe@rambler.ru':'2807349CLUZie',
    'towqdsigmc@rambler.ru':'48481486UnoRg',
    'eyzwvxphxz@rambler.ru':'5532563Bskght',
    'aruhbkpsud@rambler.ru':'8022722dNUe59',
    'kckwnnvmwf@rambler.ru':'77502899D6ygI',
    'emicquwuxf@rambler.ru':'2982514obBgCJ',
    'pnefqbonja@rambler.ru':'1443294ZY7BgB',
    'wlnecrzvkb@rambler.ru':'2016456ke4QRw',
    'lucufydobd@rambler.ru':'4188202gvlmuR',
    'obcheovoqy@rambler.ru':'34012721sYlv3',
    'fjxwhhlhxp@rambler.ru':'1621680a9CbS0',
    'rjggfmhckx@rambler.ru':'4470958ocoPjD',
    'oqixhlbhlh@rambler.ru':'4902150aD8Tkr',
    'zmlfdygkce@rambler.ru':'4809956HgOdyu',
    'zdjqfhdafp@rambler.ru':'9142498RW8Ynh',
    'cjoyoxsdby@rambler.ru':'108516737An82',
    'hfrcbbwzgb@rambler.ru':'1732107RUVvSu',
    'crkbywjfzg@rambler.ru':'9616254qbUhAG',
    'luygpfibra@rambler.ru':'9488606qXIvQZ',
    'xepjtcrrzo@rambler.ru':'3774977dMOr4c',
    'ayrbethwst@rambler.ru':'4658060glYVyA',
    'czhjnqqgdd@rambler.ru':'89865789wXqfK',
    'oltotetppj@rambler.ru':'0936665mJL9H0',
    'eaoeqvygrv@rambler.ru':'5348316HcEpsm',
    'dkfvwvkotb@rambler.ru':'3366454MTGiOR',
    'wavsfqiarg@rambler.ru':'4220587wVJ8gU',
    'gkwlbrhwix@rambler.ru':'6383580cCHutT',
    'uachryyzde@rambler.ru':'0643369cWRWhr',
    'nuyfldwirg@rambler.ru':'29709163eKxWc',
    'fnorovxtvk@rambler.ru':'469173140zLer',
    'qrmnfyxdqj@rambler.ru':'7609701E9XfBC',
    'ncupywgysj@rambler.ru':'8506439mTgrb6',
    'ehhuextqqm@rambler.ru':'4136418EqGa4N',
    'utasiosnxd@rambler.ru':'6230428wOiMLm',
    'ppizzpzqod@rambler.ru':'6217530deEIGb',
    'mgzczmjjpo@rambler.ru':'5974114gf7VLz',
    'ezugyxxfkx@rambler.ru':'6920685aZVulS',
    'vnuwwwuhuj@rambler.ru':'20889562nRk1x',
    'xqkicchcbc@rambler.ru':'4345126XoitUD',
    'hykbjrvqsw@rambler.ru':'8281493mLUbNt',
    'etyqikxlam@rambler.ru':'1096360Cvg5n7',
    'blnpfilkdh@rambler.ru':'6208964Fhgy1O',
    'azawxjcfeh@rambler.ru':'8923382Pqo1jI',
    'dyumumpgus@rambler.ru':'3454195S5FQ7d',
    'ryejfejmef@rambler.ru':'1474062Y49oZE',
    'uqyfeqyumv@rambler.ru':'4305431o270vK',
    'vardlzqzas@rambler.ru':'8158325VAjymq',
    'wvqbwbpofd@rambler.ru':'2037592lvIWZI',
    'agsnpvxscg@rambler.ru':'676450330Gmzj',
    'ctiwtwpowk@rambler.ru':'7004605qQOK5O',
    'vvluscokds@rambler.ru':'2351339uVtaUb',
    'gqtipysiyk@rambler.ru':'4672575GMSkQq',
    'vwtjzupcul@rambler.ru':'6978060SRfKxQ',
    'klvdgsoczb@rambler.ru':'8504791kNehzf',
    'lavpussyin@rambler.ru':'1183746FmKlfU',
    'xvzoptqyhd@rambler.ru':'7635851M7gCQO',
    'yzkgydxjlr@rambler.ru':'3889248nBv9xb',
    'tkuscgummb@rambler.ru':'2646861vfBmjy',
    'ytbfnnlvuc@rambler.ru':'8680715wXqNoY',
    'qrmyueqrpk@rambler.ru':'48163158cQzn3',
    'nulburzrsp@rambler.ru':'4628721fbFYDx',
    'xpsncakaar@rambler.ru':'8050121QgZtLE',
    'rsfyuinlhi@rambler.ru':'7789677doEl7X',
    'lruwhkjpmm@rambler.ru':'2407934PCrhbt',
    'zqlboekoph@rambler.ru':'4540547BXedBD',
    'djrmgdvpxk@rambler.ru':'2516345lt4GhI',
    'cdyagajvqt@rambler.ru':'0457036J8b9x1',
    'csbmtfyogo@rambler.ru':'8578398RoY5Me',
    'mtgjgvchbf@rambler.ru':'6273263XOh0fb',
    'hjovrkraea@rambler.ru':'1756354e4T9PL',
    'wuasdmqayg@rambler.ru':'8983467Njjbfc',
    'dnzaquycrh@rambler.ru':'3047369gLtNHO',
    'rdptnhimnz@rambler.ru':'92217639LcTX1',
    'yklofyaekj@rambler.ru':'0018913JhfLfv',
    'zqfzplzlwp@rambler.ru':'6550676M1gwNy',
    'fzcveyejbh@rambler.ru':'9098104PB57ol',
    'qcpwhpqape@rambler.ru':'3277585gafS4o',
    'xfitvnzvez@rambler.ru':'0023433CgWWiW',
    'tiansbolvj@rambler.ru':'0200419d6c8hD',
    'ibwukvjyxn@rambler.ru':'6846348Go4rB7',
    'tfclkifgjn@rambler.ru':'9973469KBqk2S',
    'yscehsgepj@rambler.ru':'0258935Wptd0G',
    'webznumpmf@rambler.ru':'4342482ZhTyVk',
    'xadehtuxys@rambler.ru':'94129234ZK2kl',
    'wsfmuqnmjp@rambler.ru':'7886187uCcru0',
    'mhovkuzfnl@rambler.ru':'3632660bLpvSw',
    'pppuvtsuxu@rambler.ru':'6227635FqgnGa',
    'vvezjeryic@rambler.ru':'7595367ZgjYIn',
    'oiukjktkhx@rambler.ru':'35863397YZBFb',
    'qswbndmblj@rambler.ru':'3563325a93EZ6',
    'ztyfnsdrqa@rambler.ru':'7748929ZbfDrw',
    'lrjduagkcj@rambler.ru':'8783147DV4pJe',
    'fhrzanukuh@rambler.ru':'169703230lEf6',
    'pqnnzwuuku@rambler.ru':'6446752B0qw8H',
    'ndctkqjnfc@rambler.ru':'1534939xHfafC',
    'tlzuekovcn@rambler.ru':'9668644RKjMla',
    'ermdcrjyhu@rambler.ru':'9838788xXiLRC',
    'qbfymlhpwj@rambler.ru':'3278597BlWafL',
    'uuuzmgapoy@rambler.ru':'2535811Vz3dxV',
    'chjolhsihy@rambler.ru':'8253848P8B5cd',
    'rrakdmtsdb@rambler.ru':'0459246V4tjHK',
    'ngkrbvqvha@rambler.ru':'9835759JQxkal',
    'caxeoztjpa@rambler.ru':'1297098SSweKM',
    'molnxkchzu@rambler.ru':'3122920NIh3iE',
    'murnslgulf@rambler.ru':'1045964Oppb9c',
    'twicbfjgoz@rambler.ru':'0187832xjeOz1',
}

# Почты поддержки
receivers = ['sms@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org', 'sticker@telegram.org', 'support@telegram.org']

# =========================================================
# БЛОК 2: SMTP ФУНКЦИЯ (ДВИЖОК)
# =========================================================
def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        if 'gmail.com' in sender_email:
            smtp_server, smtp_port = 'smtp.gmail.com', 587
        elif 'rambler.ru' in sender_email:
            smtp_server, smtp_port = 'smtp.rambler.ru', 587
        elif 'mail.ru' in sender_email:
            smtp_server, smtp_port = 'smtp.mail.ru', 465
        else:
            smtp_server, smtp_port = 'smtp.gmail.com', 587
        
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False

# =========================================================
# БЛОК 3: ИНТЕРФЕЙС И ГЛАВНАЯ ЛОГИКА
# =========================================================
def main():
    banner = '''
    ███████╗███╗   ██╗ ██████╗ ███████╗███████╗██████╗ 
    ██╔════╝████╗  ██║██╔═══██╗██╔════╝██╔════╝██╔══██╗
    ███████╗██╔██╗ ██║██║   ██║███████╗█████╗  ██████╔╝
    ╚════██║██║╚██╗██║██║   ██║╚════██║██╔══╝  ██╔══██╗
    ███████║██║ ╚████║╚██████╔╝███████║███████╗██║  ██║
    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
    '''
    print(Colorate.Horizontal(Colors.blue_to_red, banner))
    
    print("🔱 [1] СНОС АККАУНТОВ  [2] СНОС КАНАЛОВ")
    print("🔱 [3] СНОС БОТОВ       [4] СНОС ЧАТОВ")
    print("🔱 [5] ПРОБИВ (OSINT)  [6] ПОИСК ПО БАЗЕ")
    print("🔱 [7] СНОС ДОКСА/СЛИВА")
    
    choice = input("\nВыбор пункта > ")

    if choice in ['1', '2', '3', '4']:
        # Стандартная логика репортов
        username = input("USERNAME (через @): ")
        tg_id = input("TG ID: ")
        violation_link = input("ССЫЛКА НА НАРУШЕНИЕ: ")
        text = f"Target: {username} (ID: {tg_id}). Proof: {violation_link}. Policy Violation."
        
        print("\n--- АТАКА НАЧАЛАСЬ ---")
        for s_email, s_pass in senders.items():
            for r_email in receivers:
                if send_email(r_email, s_email, s_pass, "Report", text):
                    print(f"[+] Отправлено с {s_email}")
                time.sleep(1)

    elif choice == '5':
        # Пробив по мануалу LoytWin
        cprint("\n--- МОДУЛЬ ПРОБИВА (LOYTWIN 303) ---", "yellow")
        target = input("ВВЕДИ НОМЕР ИЛИ НИК: ")
        print(f"\n[!] Ссылки для чека {target}:")
        print(f"-> Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"-> База Казахстана: https://fa-fa.kz/search?query={target}")
        print(f"-> Теги: https://phoneradar.ru/phone/{target}")
        print("\n[!] Юзай ботов: @GlazGun_bot, @Okskskekbot, @userbox_search_bot")
        input("\nНажми Enter...")

    elif choice == '6':
        # Поиск по Zambia CSV
        cprint("\n--- ПОИСК ПО ЛОКАЛЬНОЙ БАЗЕ ---", "magenta")
        search_q = input("ВВЕДИ ФИО ИЛИ EMAIL: ").lower()
        file_name = "Zambia.xls - Sheet 1.csv"
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                found = False
                for line in f:
                    if search_q in line.lower():
                        cprint(f"[+] НАЙДЕНО: {line.strip()}", "green")
                        found = True
                if not found: print("[-] Нет данных.")
        else:
            print("[-] Файл базы не найден.")
        input("\nEnter...")

    elif choice == '7':
        # Снос докса (репорт на слив данных)
        target_link = input("ССЫЛКА НА ПОСТ С ДОКСОМ: ")
        text = f"Hello. Post {target_link} contains leaked private data. Remove it."
        print("\n--- ЗАЧИСТКА ДОКСА ---")
        for s_email, s_pass in senders.items():
            for r_email in receivers:
                send_email(r_email, s_email, s_pass, "Privacy Violation", text)
                print(f"[+] Репорт отправлен: {s_email}")
        time.sleep(2)

if __name__ == "__main__":
    main()     # НОВЫЙ БЛОК 8: КОНСТРУКТОР ОТЧЕТА (ДЕАНОН)
    elif choice == '8':
        cprint("\n--- ГЕНЕРАЦИЯ ОТЧЕТА ПО ШАБЛОНУ ---", "cyan")
        
        # Собираем данные
        author = input("Автор: ")
        reason = input("Причина: ")
        fio = input("Ф.И.О: ")
        dob = input("Дата рождения: ")
        phone = input("Номер телефона: ")
        address = input("Адрес: ")
        email = input("Email: ")
        vk = input("VK: ")
        insta = input("Instagram: ")
        tg_user = input("TG Username: ")
        tg_id = input("TG ID: ")
        passport = input("Паспортные данные: ")
        auto_num = input("Гос номер авто: ")
        
        # Формируем шаблон из файла
        report = f"""
  ____            _     _       
 |  _ \  _____  _| |__ (_)_ __  
 | | | |/ _ \ \/ / '_ \| | '_ \ 
 | |_| | (_) >  <| |_) | | | | |
 |____/ \___/_/\_\_.__/|_|_| |_| 

× Автор: {author}
× Причина доксинга: {reason}

—×--×--×--×--×--×--×—
 -×- Персональная информация -×-
× Ф.И.О → {fio}
× Дата рождения → {dob}
× Номер телефона → {phone}
× Адрес → {address}
× Email → {email}
—×--×--×--×--×--×--×—
 -×- Социальные сети/мессенджеры -×-
× Страница VK → {vk}
× Instagram страница → {insta}
× Telegram username → {tg_user}
× Telegram ID → {tg_id}
—×--×--×--×--×--×--×—
 -×- Информация о документах -×-
× Паспортные данные → {passport}
—×--×--×--×--×--×--×—
 -×- Информация об автомобиле -×-
× Гос номер → {auto_num}
—×--×--×--×--×--×--×—
        """
        
        # Вывод и сохранение
        print("\n" + report)
        save = input("Сохранить в файл? (y/n): ")
        if save.lower() == 'y':
            with open(f"dox_{tg_id}.txt", "w", encoding="utf-8") as f:
                f.write(report)
            print(f"[+] Отчет сохранен как dox_{tg_id}.txt")
        input("\nНажми Enter для возврата...") 
def main():
    banner = '''
    ███████╗███╗   ██╗ ██████╗ ███████╗███████╗██████╗ 
    ██╔════╝████╗  ██║██╔═══██╗██╔════╝██╔════╝██╔══██╗
    ███████╗██╔██╗ ██║██║   ██║███████╗█████╗  ██████╔╝
    ╚════██║██║╚██╗██║██║   ██║╚════██║██╔══╝  ██╔══██╗
    ███████║██║ ╚████║╚██████╔╝███████║███████╗██║  ██║
    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
    '''
    print(Colorate.Horizontal(Colors.blue_to_red, banner))
    
        print("🔱 [1] СНОС АККАУНТОВ  [2] СНОС КАНАЛОВ")
    print("🔱 [3] СНОС БОТОВ       [4] СНОС ЧАТОВ")
    print("🔱 [5] СНОС ДОКСА       [6] УЛЬТИМАТИВНЫЙ ПРОБИВ (БАЗЫ + OSINT)")
    print("🔱 [7] СОСТАВИТЬ ОТЧЕТ (PRO)")

    
    choice = input("\nВыбор пункта > ")

    # Блоки 1-4: Репорты
    if choice in ['1', '2', '3', '4']:
        username = input("USERNAME: ")
        tg_id = input("TG ID: ")
        v_link = input("ССЫЛКА НА НАРУШЕНИЕ: ")
        text = f"Target: {username} (ID: {tg_id}). Violation proof: {v_link}."
        print("\n--- АТАКА ЗАПУЩЕНА ---")
        for s_email, s_pass in senders.items():
            for r_email in receivers:
                if send_email(r_email, s_email, s_pass, "Report", text):
                    print(f"[+] Отправлено: {s_email}")
                time.sleep(0.5)

    # Блок 5: Справочник OSINT
    elif choice == '5':
        cprint("\n--- MANUAL BY LOYTWIN ---", "yellow")
        target = input("ВВЕДИ ДАННЫЕ: ")
        print(f"Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"Казахстан (Fa-Fa): https://fa-fa.kz/search?query={target}")
        input("\nEnter...")
    # ОБЪЕДИНЕННЫЙ БЛОК 6: ВСЁ В ОДНОМ
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПОИСК ПО ВСЕМ ДАННЫМ ---", "magenta")
        target = input("ВВЕДИ НОМЕР, НИК ИЛИ ФИО: ").lower()
        
        # 1. Поиск по локальным базам (CSV)
        dbs = ["Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv"]
        found = False
        print(f"[*] Ищу в локальных базах...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        # 2. Генерация ссылок для ручного пробива
        print(f"\n[*] Ссылки для доп. проверки:")
        print(f"🔗 Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"🔗 Казахстан (Fa-Fa): https://fa-fa.kz/search?query={target}")
        print(f"🔗 Поиск в Google: https://www.google.com/search?q={target}")
        
        if not found:
            print("\n[-] В локальных базах совпадений не найдено.")
        input("\nНажми Enter для возврата...")

    # БЛОК 7: ГЕНЕРАЦИЯ ОТЧЕТА (ШАБЛОН 312)
    elif choice == '7':
        cprint("\n--- КОНСТРУКТОР ОТЧЕТА ---", "cyan")
        fio = input("ФИО: ")
        phone = input("Номер: ")
        tg_id = input("TG ID: ")
        # Сюда можно добавить еще input'ы для СНИЛС, ИНН и т.д.
        
        report = f"""
  ____            _     _       
 |  _ \\  _____  _| |__ (_)_ __  
 | | | |/ _ \\ \\/ / '_ \\| | '_ \\ 
 | |_| | (_) >  <| |_) | | | | |
 |____/ \\___/_/\\_\\_.__/|_|_| |_| 

-×- ПЕРСОНАЛЬНАЯ ИНФОРМАЦИЯ -×-
× Ф.И.О → {fio}
× Номер телефона → {phone}
× Telegram ID → {tg_id}
—×--×--×--×--×--×--×—
        """
        print("\n" + report)
        if input("Сохранить файл? (y/n): ").lower() == 'y':
            with open(f"Dox_{tg_id}.txt", "w", encoding="utf-8") as f:
                f.write(report)
            print("[+] Сохранено.")
        input("\nEnter...")
    # ОБНОВЛЕННЫЙ БЛОК 6: УЛЬТИМАТИВНЫЙ ПРОБИВ + ПОИСК ФОТО
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПРОБИВ И ПОИСК ФОТО ---", "magenta")
        target = input("ВВЕДИ НОМЕР, НИК, ФИО ИЛИ ID: ").lower()
        
        # 1. Поиск по локальным базам (Zambia, Switzerland)
        dbs = ["Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv"]
        found = False
        print(f"[*] Проверка локальных баз данных...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО В {db}: {line.strip()}", "green")
                            found = True
        
        # 2. Модуль поиска фото (на основе твоего обучения)
        print(f"\n--- МЕТОДЫ ПОИСКА ФОТО (ОБУЧЕНИЕ) ---")
        print(f"📍 Способ №1 (Google/Yandex):")
        print(f"   Запрос для Яндекса: intext:{target}")
        print(f"   (Ищи в разделе 'Картинки' для поиска старых публикаций)")
        
        print(f"\n📍 Способ №2 (Соцсети):")
        print(f"   Проверь старые страницы в ВК, ОК, Instagram и WhatsApp.")
        
        print(f"\n📍 Способ №3 (Боты):")
        print(f"   Используй @TG_NoNameBot (отправь ему ссылку на ВК)")

        # 3. Быстрые ссылки
        print(f"\n--- БЫСТРЫЕ ССЫЛКИ ---")
        print(f"🔗 Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"🔗 Казахстан (Fa-Fa): https://fa-fa.kz/search?query={target}")
        print(f"🔗 Поиск ID ВК: https://vk.com/search?c%5Bsection%5D=people&c%5Bq%5D={target}")
        
        if not found:
            print("\n[-] В базах совпадений нет, используй методы поиска выше.")
        input("\nНажми Enter для возврата...")

    # ОБНОВЛЕННЫЙ СПИСОК КОМАНД (для меню)
    # print("🔱 [6] УЛЬТИМАТИВНЫЙ ПРОБИВ + ПОИСК ФОТО")
    # print("🔱 [7] СОСТАВИТЬ ОТЧЕТ (PRO)") 
    # ОБНОВЛЕННЫЙ БЛОК 6: УЛЬТИМАТИВНЫЙ ПРОБИВ (ВСЕ БАЗЫ + ФОТО + USA ERRORS)
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПРОБИВ (+ USA EXPORT ERRORS) ---", "magenta")
        target = input("ВВЕДИ ДАННЫЕ (НИК/ФИО/ID/ТЕЛ): ").lower()
        
        # Список всех твоих баз данных
        dbs = [
            "Zambia.xls - Sheet 1.csv", 
            "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv"
        ]
        
        found = False
        print(f"[*] Сканирую локальные базы...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО В {db}: {line.strip()}", "green")
                            found = True
        
        # Инструкция по фото (из файла Обучение)
        print(f"\n--- МЕТОДЫ ПОИСКА ФОТО ---")
        print(f"📍 Яндекс: intext:{target} (раздел Картинки)")
        print(f"📍 Бот: @TG_NoNameBot (через ссылку ВК)")
        
        # Быстрые OSINT-ссылки
        print(f"\n--- БЫСТРЫЕ ССЫЛКИ ---")
        print(f"🔗 Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"🔗 Fa-Fa (KZ): https://fa-fa.kz/search?query={target}")
        
        if not found:
            print("\n[-] В локальных файлах совпадений нет.")
        input("\nНажми Enter для возврата...")

    # БЛОК 7: ОТЧЕТ (ПРОДВИНУТЫЙ ШАБЛОН)
    elif choice == '7':
        cprint("\n--- СОЗДАНИЕ ОТЧЕТА ---", "cyan")
        fio = input("ФИО: ")
        id_tg = input("TG ID: ")
        
        report = f"""
  ____            _     _       
 |  _ \\  _____  _| |__ (_)_ __  
 | | | |/ _ \\ \\/ / '_ \\| | '_ \\ 
 | |_| | (_) >  <| |_) | | | | |
 |____/ \\___/_/\\_\\_.__/|_|_| |_| 

× Ф.И.О → {fio}
× Telegram ID → {id_tg}
—×--×--×--×--×--×--×—
        """
        print("\n" + report)
        if input("Сохранить? (y/n): ").lower() == 'y':
            with open(f"Dox_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report)
        input("\nEnter...")

# Закрытие программы
if __name__ == "__main__":
    main() 
    # ОБНОВЛЕННЫЙ БЛОК 6: УЛЬТИМАТИВНЫЙ ПРОБИВ (Zambia, Switzerland, USA, Taiwan + Фото)
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПРОБИВ ПО ВСЕМ БАЗАМ ---", "magenta")
        target = input("ВВЕДИ ДАННЫЕ (НИК/ФИО/ID/ТЕЛ): ").lower()
        
        # Полный список всех твоих баз
        dbs = [
            "Zambia.xls - Sheet 1.csv", 
            "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv",
            "Taiwan.xls - Sheet 1.csv"
        ]
        
        found = False
        print(f"[*] Запуск сканирования локальных баз...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО В {db}: {line.strip()}", "green")
                            found = True
        
        # Методы поиска фото из обучения
        print(f"\n--- ИНСТРУКЦИЯ ПО ПОИСКУ ФОТО ---")
        print(f"📸 Яндекс Картинки: запрос 'intext:{target}'")
        print(f"📸 Поиск по соцсетям: ВК, ОК, Inst, WhatsApp")
        print(f"📸 Бот для фото: @TG_NoNameBot (через ссылку ВК)")
        
        # OSINT ссылки
        print(f"\n--- ВНЕШНИЕ ССЫЛКИ ---")
        print(f"🔗 Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"🔗 Fa-Fa (Казахстан): https://fa-fa.kz/search?query={target}")
        
        if not found:
            print("\n[-] В локальных базах (включая Тайвань) совпадений нет.")
        input("\nНажми Enter для возврата...")

    # БЛОК 7: ГЕНЕРАТОР ОТЧЕТА (PRO)
    elif choice == '7':
        cprint("\n--- КОНСТРУКТОР ОТЧЕТА ---", "cyan")
        # Собираем основные данные
        fio = input("Ф.И.О: ")
        id_tg = input("TG ID: ")
        phone = input("Номер телефона: ")
        
        report = f"""
  ____            _     _       
 |  _ \\  _____  _| |__ (_)_ __  
 | | | |/ _ \\ \\/ / '_ \\| | '_ \\ 
 | |_| | (_) >  <| |_) | | | | |
 |____/ \\___/_/\\_\\_.__/|_|_| |_| 

-×- ПЕРСОНАЛЬНАЯ ИНФОРМАЦИЯ -×-
× Ф.И.О → {fio}
× Номер телефона → {phone}
× Telegram ID → {id_tg}
—×--×--×--×--×--×--×—
        """
        print("\n" + report)
        if input("Сохранить в файл? (y/n): ").lower() == 'y':
            with open(f"Dox_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report)
            print(f"[+] Файл Dox_{id_tg}.txt успешно создан.")
        input("\nEnter...")

# Конец программы
if __name__ == "__main__":
    main()
# === НОВЫЙ УЛЬТИМАТИВНЫЙ БЛОК (ДОБАВИТЬ В КОНЕЦ) ===
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПРОБИВ ПО ВСЕМ ОБНОВЛЕННЫМ БАЗАМ ---", "magenta")
        target = input("ВВЕДИ ДАННЫЕ (НИК/ФИО/ID/ТЕЛ): ").lower()
        
        # Полный список твоих загруженных баз
        dbs = [
            "Zambia.xls - Sheet 1.csv", 
            "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv",
            "Taiwan.xls - Sheet 1.csv",
            "Thailand.xls - Sheet 1.csv"
        ]
        
        found = False
        print(f"[*] Сканирую файлы стран...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            # Выводит название страны и найденную строку
                            country = db.split('.')[0]
                            cprint(f"[+] НАЙДЕНО [{country}]: {line.strip()}", "green")
                            found = True
        
        # МЕТОДЫ ПОИСКА ФОТО (на основе твоего файла обучения)
        print(f"\n--- ПОИСК СТАРЫХ ФОТО ---")
        print(f"📸 Яндекс: используй запрос 'intext:{target}' в Картинках")
        print(f"📸 Соцсети: проверь старые страницы ВК, ОК и профиль в WhatsApp")
        print(f"📸 Telegram: бот @TG_NoNameBot (отправь ссылку на ВК)")
        
        # OSINT ССЫЛКИ
        print(f"\n--- БЫСТРЫЕ ССЫЛКИ ---")
        print(f"🔗 Авто (РФ): https://www.nomerogram.ru/n/{target}")
        print(f"🔗 База (KZ): https://fa-fa.kz/search?query={target}")
        
        if not found:
            print("\n[-] В локальных CSV-файлах совпадений не найдено.")
        input("\nНажми Enter для возврата...")

    elif choice == '7':
        cprint("\n--- КОНСТРУКТОР ОТЧЕТА (PRO) ---", "cyan")
        # Здесь можно расширить ввод данных по шаблону 312
        fio = input("ФИО: ")
        id_tg = input("TG ID: ")
        
        report = f"--- ОТЧЕТ ---\nФИО: {fio}\nID: {id_tg}\n--------------"
        print("\n" + report)
        if input("Сохранить? (y/n): ").lower() == 'y':
            with open(f"Result_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report)
        input("\nEnter...")  # === НОВЫЙ БЛОК: РАСШИРЕННЫЙ ПРОБИВ + ПРИВАТНЫЕ ССЫЛКИ (ДОБАВИТЬ В КОНЕЦ) ===
    elif choice == '6':
        cprint("\n--- УЛЬТИМАТИВНЫЙ ПОИСК (БАЗЫ + ПРИВАТНЫЕ OSINT ССЫЛКИ) ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС (ФИО/НИК/ID/ТЕЛ): ").lower()
        
        # Обновленный список всех твоих баз (включая Таиланд)
        dbs = [
            "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
            "Thailand.xls - Sheet 1.csv"
        ]
        
        found = False
        print(f"[*] Сканирование локальных файлов...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        # НОВЫЕ ПРИВАТНЫЕ ССЫЛКИ ИЗ ОБУЧЕНИЯ REYZOV
        print(f"\n--- ПРИВАТНЫЕ ИНСТРУМЕНТЫ (REYZOV) ---")
        print(f"🕵️ Скрытые друзья ВК: http://220vk.com/ | http://vk.city4me.com/")
        print(f"📂 Архивы (кэш): http://archive.is/ | http://www.cachedpages.com/")
        print(f"📑 Документы: ИНН (https://service.nalog.ru/inn.html) | Паспорт (http://services.fms.gov.ru)")
        print(f"🤖 Приватный бот: @RedSearchBot")
        
        # Методы поиска фото
        print(f"\n--- МЕТОДЫ ПОИСКА ФОТО ---")
        print(f"📸 Яндекс: intext:{target} (раздел Картинки)")
        print(f"📸 Бот для фото: @TG_NoNameBot")
        
        # Внешние ресурсы
        print(f"\n--- ДОПОЛНИТЕЛЬНО ---")
        print(f"🔗 Номерограмм: https://www.nomerogram.ru/n/{target}")
        print(f"🔗 Fa-Fa KZ: https://fa-fa.kz/search?query={target}")
        
        if not found:
            print("\n[-] В локальных базах данных нет совпадений.")
        input("\nНажми Enter для возврата...")

    elif choice == '7':
        cprint("\n--- КОНСТРУКТОР ОТЧЕТА ---", "cyan")
        fio = input("ФИО: ")
        id_tg = input("TG ID: ")
        
        report = f"--- ОТЧЕТ ---\nФИО: {fio}\nID: {id_tg}\n--------------"
        print("\n" + report)
        if input("Сохранить результат? (y/n): ").lower() == 'y':
            with open(f"Result_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report)
        input("\nEnter...")     # === НОВЫЙ БЛОК: ПОИСК ПО НИКУ (ДОБАВИТЬ В КОНЕЦ) ===
    elif choice == '6':
        cprint("\n--- УЛЬТИМАТИВНЫЙ ПОИСК (БАЗЫ + НИКНЕЙМЫ + OSINT) ---", "magenta")
        target = input("ВВЕДИ НИК, ТЕЛЕФОН ИЛИ ФИО: ").lower()
        
        # Список всех баз
        dbs = [
            "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
            "Thailand.xls - Sheet 1.csv"
        ]
        
        found = False
        print(f"[*] Проверка локальных баз...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        # НОВЫЙ МОДУЛЬ: ПОИСК ПО НИКУ (из файла ник (1).txt)
        print(f"\n--- ПОИСК ПО НИКНЕЙМУ (OSINT) ---")
        print(f"🔗 Быстрая проверка: https://whatsmyname.app/")
        print(f"🔗 Проверка сервисов: https://namecheckup.com/ | https://instantusername.com/")
        print(f"🔗 Поиск по форумам: https://boardreader.com/")
        print(f"🔗 Утечки и пароли: https://leakedsource.ru/ | @mailsearchbot")
        print(f"🔗 Сложный поиск (300+ сервисов): https://suip.biz/")
        
        # Ссылки из прошлых мануалов (Reyzov и Фото)
        print(f"\n--- ПРИВАТНЫЕ ИНСТРУМЕНТЫ И ФОТО ---")
        print(f"🕵️ Скрытые друзья ВК: http://220vk.com/")
        print(f"📸 Яндекс Картинки: intext:{target}")
        print(f"🤖 Боты: @RedSearchBot | @TG_NoNameBot")
        
        if not found:
            print("\n[-] В локальных базах совпадений нет, работай по ссылкам выше.")
        input("\nНажми Enter для возврата...")

    elif choice == '7':
        cprint("\n--- ГЕНЕРАТОР ОТЧЕТА ---", "cyan")
        fio = input("ФИО: ")
        id_tg = input("TG ID: ")
        
        report = f"--- ОТЧЕТ ---\nФИО: {fio}\nID: {id_tg}\n--------------"
        print("\n" + report)
        if input("Сохранить результат? (y/n): ").lower() == 'y':
            with open(f"Result_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report)
        input("\nEnter...") 
# === НОВЫЙ БЛОК: УЛЬТИМАТИВНЫЙ ПРОБИВ + БОТЫ (ROXY MANUAL) ===
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПРОБИВ (БАЗЫ + НИКИ + ТГ БОТЫ) ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС (НИК/ТЕЛ/ФИО/ID): ").lower()
        
        # Список всех локальных баз
        dbs = [
            "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
            "Thailand.xls - Sheet 1.csv"
        ]
        
        found = False
        print(f"[*] Проверка локальных CSV баз...")
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        # НОВЫЙ МОДУЛЬ: ТЕЛЕГРАМ БОТЫ (из мануала Roxy)
        print(f"\n--- ЛУЧШИЕ БОТЫ ДЛЯ ПРОБИВА (ROXY) ---")
        print(f"🤖 Базы и адреса: @pyth1a_0racle_bot | @Probivevelocmo_bot")
        print(f"🤖 Соцсети и город: @visionerobot | @InfoVkUser_bot")
        print(f"🤖 Поиск по авто: @CarPlatesUkraineBot | @ogrn_bot")
        print(f"🤖 Спец. поиск: @Quick_osintik_bot | @infobazaa_bot")
        print(f"🤖 Вирт. номера: @smsactivate_bot | @AuroraSMS_bot")
        
        # Инструменты из прошлых файлов (Ники, Реизов, Фото)
        print(f"\n--- ПРИВАТНЫЕ OSINT ССЫЛКИ ---")
        print(f"🔗 Никнеймы: https://whatsmyname.app/ | https://suip.biz/")
        print(f"🔗 ВК и Документы: http://220vk.com/ | https://service.nalog.ru/inn.html")
        print(f"📸 Фото: Яндекс 'intext:{target}' | @TG_NoNameBot")
        
        if not found:
            print("\n[-] В локальных базах пусто. Используй ботов и ссылки выше.")
        input("\nНажми Enter для возврата...")

    elif choice == '7':
        cprint("\n--- КОНСТРУКТОР ОТЧЕТА ---", "cyan")
        fio = input("ФИО: ")
        id_tg = input("TG ID: ")
        
        report = f"--- ОТЧЕТ ---\nФИО: {fio}\nID: {id_tg}\n--------------"
        print("\n" + report)
        if input("Сохранить результат? (y/n): ").lower() == 'y':
            with open(f"Result_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report)
        input("\nEnter...")
    # === НОВЫЙ БЛОК: СОВЕТЫ ПО РАЗРАБОТКЕ (ИЗ БИБЛИИ RENC'A) ===
    elif choice == '8':
        cprint("\n--- ГИД ПО УЛУЧШЕНИЮ СОФТА (BY RENC) ---", "yellow")
        print("1. 🛠 Языки: Для сетей — JS, для систем и баз — C#, для души — Python.")
        print("2. 🎨 Интерфейс: Консоль — это база, но пора учить PyQt5 для GUI.")
        print("3. ✨ Уникальность: Не копируй чужое, придумай свою фишку (анимацию, логику).")
        print("4. 🛡 Безопасность: Учи базу (XSS и прочее), чтобы софт был надежным.")
        cprint("\n[!] Главное — не лениться и вкладываться в детали.", "red")
        input("\nНажми Enter для возврата...")

    # ОБНОВЛЕННЫЙ БЛОК 6 (ДОПОЛНЕН ИЗ ВСЕХ ТВОИХ ФАЙЛОВ)
    elif choice == '6':
        cprint("\n--- GLOBAL ULTIMATE SEARCH ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС: ").lower()
        
        # Все твои базы
        dbs = ["Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv", 
               "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv", 
               "Thailand.xls - Sheet 1.csv"]
        
        found = False
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        # Интеграция ссылок из всех мануалов (Reyzov, Roxy, Ник)
        print(f"\n--- OSINT ИНСТРУМЕНТЫ ---")
        print(f"🔗 Никнеймы: https://whatsmyname.app/ | https://suip.biz/")
        print(f"🤖 Топ Боты: @RedSearchBot | @pyth1a_0racle_bot | @visionerobot")
        print(f"📸 Фото: Яндекс 'intext:{target}' | @TG_NoNameBot")
        print(f"🕵️ Приват: http://220vk.com/ | https://service.nalog.ru/inn.html")
        
        input("\nНажми Enter...")

    elif choice == '7':
        cprint("\n--- ОТЧЕТ ---", "cyan")
        fio = input("ФИО: "); id_tg = input("TG ID: ")
        report = f"--- REPORT ---\nФИО: {fio}\nID: {id_tg}\n--------------"
        print("\n" + report)
        if input("Сохранить? (y/n): ").lower() == 'y':
            with open(f"Result_{id_tg}.txt", "w", encoding="utf-8") as f: f.write(report)
        input("\nEnter...")
    # === НОВЫЙ БЛОК: МЕТОДЫ ВОССТАНОВЛЕНИЯ (ДОБАВИТЬ В КОНЕЦ) ===
    elif choice == '9':
        cprint("\n--- ДЕАНОН ЧЕРЕЗ ВОССТАНОВЛЕНИЕ АККАУНТОВ ---", "yellow")
        print("📍 Эти ссылки помогут узнать маскированную почту или номер телефона (например, +7***12):")
        print("🔗 VK: https://vk.com/restore")
        print("🔗 Mail.ru: https://account.mail.ru/recovery")
        print("🔗 Facebook: https://facebook.com/login/identify")
        print("🔗 Twitter: https://twitter.com/password/reset")
        print("🔗 Instagram: https://instagram.com/accounts/password/reset")
        print("\n💡 Совет: Также используй мобильные приложения WebMoney и Instagram для поиска по контактам.")
        input("\nНажми Enter для возврата...")

    # ОБНОВЛЕННЫЙ БЛОК 6 (ДОБАВИЛ ССЫЛКИ ДЛЯ ВОССТАНОВЛЕНИЯ СЮДА ТОЖЕ)
    elif choice == '6':
        cprint("\n--- GLOBAL ULTIMATE SEARCH ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС: ").lower()
        
        dbs = ["Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv", 
               "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv", 
               "Thailand.xls - Sheet 1.csv"]
        
        found = False
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        print(f"\n--- OSINT ИНСТРУМЕНТЫ И ВОССТАНОВЛЕНИЕ ---")
        print(f"🔑 Узнать данные через: VK Restore, Mail.ru Recovery")
        print(f"🔗 Никнеймы: https://whatsmyname.app/")
        print(f"🤖 Боты: @RedSearchBot | @visionerobot | @pyth1a_0racle_bot")
        print(f"📸 Фото: Яндекс 'intext:{target}'")
        
        input("\nНажми Enter...")      # === НОВЫЙ БЛОК: МЕТОДЫ ВОССТАНОВЛЕНИЯ (ДОБАВИТЬ В КОНЕЦ) ===
    elif choice == '10':
        cprint("\n--- ДЕАНОН ЧЕРЕЗ ФОРМЫ ВОССТАНОВЛЕНИЯ ---", "yellow")
        print("📍 Эти сервисы при вводе логина показывают маскированные данные (+7****123 или m****@mail.ru):")
        print("🔗 Mail.ru Recovery: https://account.mail.ru/recovery")
        print("🔗 VK Restore: https://vk.com/restore")
        print("🔗 Facebook Identify: https://facebook.com/login/identify")
        print("🔗 Twitter Reset: https://twitter.com/password/reset")
        print("🔗 Instagram Reset: https://instagram.com/accounts/password/reset")
        
        print("\n📍 Проверка через мобильные приложения (поиск по контактам):")
        print("📲 WebMoney Keeper")
        print("📲 Instagram (Синхронизация контактов)")
        print("📲 Twitter / VK")
        
        cprint("\n💡 Совет: Если знаешь первые/последние цифры из баз, эти формы помогут подтвердить личность.", "blue")
        input("\nНажми Enter для возврата...")

    # ОБНОВЛЕННЫЙ БЛОК 6 (ОБЪЕДИНЕННЫЙ ПОИСК)
    elif choice == '6':
        cprint("\n--- GLOBAL ULTIMATE SEARCH ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС (ФИО/НИК/ТЕЛ/ID): ").lower()
        
        # Все твои базы
        dbs = ["Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv", 
               "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv", 
               "Thailand.xls - Sheet 1.csv"]
        
        found = False
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        print(f"\n--- БЫСТРЫЕ OSINT ИНСТРУМЕНТЫ ---")
        print(f"🤖 Боты: @RedSearchBot | @pyth1a_0racle_bot | @visionerobot")
        print(f"🔑 Восстановление: VK, Mail.ru, FB (узнать номер/почту)")
        print(f"📸 Фото: Яндекс 'intext:{target}'")
        
        input("\nНажми Enter...") 
    # === НОВЫЙ БЛОК: УКРАИНА + СОТРУДНИЧЕСТВО (ANGEL MANUAL) ===
    elif choice == '12':
        cprint("\n--- ПРОБИВ ПО УКРАИНЕ И СОТРУДНИЧЕСТВО ---", "blue")
        print("🇺🇦 Украина: @dosye_bot | @OpenDataBot | @carplates_bot (авто)")
        print("🤝 Как получить подписку бесплатно (Сотрудничество):")
        print("  • @QuickOSINT_bot — дают 30 дней за рекламу (от 1к подписоты).")
        print("  • @Zernerda_bot — дают подписку за слив новых баз данных.")
        print("  • @mailsearchbot — можно договориться о сотрудничестве через био.")
        print("🌐 Сайты: utechka.com (проверка утечек)")
        cprint("\n💡 Совет: Всегда пиши админам ботов напрямую, если есть что предложить.", "white")
        input("\nНажми Enter для возврата...")

    # ОБНОВЛЕННЫЙ БЛОК 6 (ДОБАВИЛ УКРАИНУ И НОВЫХ БОТОВ)
    elif choice == '6':
        cprint("\n--- GLOBAL ULTIMATE SEARCH ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС (ФИО/НИК/ТЕЛ/ID): ").lower()
        
        dbs = ["Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv", 
               "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv", 
               "Thailand.xls - Sheet 1.csv"]
        
        found = False
        for db in dbs:
            if os.path.exists(db):
                with open(db, 'r', encoding='utf-8') as f:
                    for line in f:
                        if target in line.lower():
                            cprint(f"[+] НАЙДЕНО ({db}): {line.strip()}", "green")
                            found = True
        
        print(f"\n--- ОБНОВЛЕННЫЕ OSINT ИНСТРУМЕНТЫ ---")
        print(f"🤖 Топ: @RedSearchBot | @pyth1a_0racle_bot | @visionerobot")
        print(f"🇺🇦 Украина: @dosye_bot | @Quick_osintik_bot")
        print(f"🔑 Восстановление: VK, Mail.ru, FB (узнать номер/почту)")
        print(f"📸 Фото: Яндекс 'intext:{target}'")
        
        input("\nНажми Enter...") 
    # === НОВЫЙ БЛОК: ОПТИМИЗИРОВАННЫЙ ПОИСК ПО ТЯЖЕЛЫМ БАЗАМ (BEELINE 24MB) ===
    elif choice == '6':
        cprint("\n--- ГЛОБАЛЬНЫЙ ПРОБИВ (ОПТИМИЗИРОВАНО ПОД БОЛЬШИЕ ФАЙЛЫ) ---", "magenta")
        target = input("ВВЕДИ ЗАПРОС (НИК/ТЕЛ/ФИО/ID): ").lower()
        
        # Список всех локальных баз
        dbs = [
            "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
            "Thailand.xls - Sheet 1.csv", "билайн юзеры.csv"
        ]
        
        found = False
        print(f"[*] Идет чтение баз данных (это может занять пару секунд)...")
        
        for db in dbs:
            if os.path.exists(db):
                # Используем генератор, чтобы не забивать оперативку файлом в 24МБ
                try:
                    with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            if target in line.lower():
                                source = "BEELINE" if "билайн" in db else db.split('.')[0]
                                cprint(f"[+] НАЙДЕНО [{source}]: {line.strip()}", "green")
                                found = True
                except Exception as e:
                    print(f"[!] Ошибка при чтении {db}: {e}")
        
        # Инструменты из последних мануалов (Angel, Roxy, Reyzov)
        print(f"\n--- ПРИВАТНЫЕ БОТЫ И СЕРВИСЫ ---")
        print(f"🤖 Украина: @dosye_bot | @carplates_bot")
        print(f"🤖 РФ/СНГ: @RedSearchBot | @visionerobot | @pyth1a_0racle_bot")
        print(f"🔑 Восстановление: VK, Mail.ru, FB (формы поиска номера)")
        print(f"📸 Фото: Яндекс 'intext:{target}' | @TG_NoNameBot")
        
        if not found:
            print("\n[-] В локальных файлах (включая Beeline) ничего не найдено.")
        input("\nНажми Enter для возврата...") 
    # === НОВЫЙ БЛОК: УЛЬТИМАТИВНЫЙ КОМБАЙН (ДОБАВИТЬ В КОНЕЦ main) ===
    elif choice == '6':
        print(f"\n{Colors.MAGENTA}--- ГЛОБАЛЬНЫЙ УЛЬТИМАТИВНЫЙ ПРОБИВ ---{Colors.END}")
        target = input(f"{Colors.CYAN}╰ Введите данные (ФИО/НИК/ТЕЛ/ID): {Colors.END}").lower()
        
        # Список всех твоих локальных баз
        dbs = [
            "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
            "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
            "Thailand.xls - Sheet 1.csv", "билайн юзеры.csv"
        ]
        
        found = False
        print(f"[*] Сканирую локальные базы (включая тяжелые файлы)...")
        
        for db in dbs:
            if os.path.exists(db):
                try:
                    # Построчное чтение для экономии памяти (важно для файлов > 20МБ)
                    with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            if target in line.lower():
                                source = "BEELINE" if "билайн" in db else db.split('.')[0]
                                print(f"{Colors.GREEN}[+] НАЙДЕНО [{source}]: {line.strip()}{Colors.END}")
                                found = True
                except Exception as e:
                    print(f"{Colors.RED}[!] Ошибка чтения {db}: {e}{Colors.END}")
        
        # Сводка инструментов из всех твоих мануалов (Angel, Roxy, Reyzov, Ренк)
        print(f"\n{Colors.YELLOW}--- ПРИВАТНЫЕ OSINT СЕРВИСЫ ---{Colors.END}")
        print(f"🌍 Украина: @dosye_bot | @OpenDataBot | @carplates_bot")
        print(f"🤖 РФ/СНГ: @RedSearchBot | @visionerobot | @pyth1a_0racle_bot")
        print(f"📸 Фото: Яндекс 'intext:{target}' | @TG_NoNameBot")
        print(f"🔗 Ники: https://whatsmyname.app/ | https://suip.biz/")
        print(f"🔑 Восстановление (узнать номер): VK, Mail.ru, FB, Insta")
        
        if not found:
            print(f"\n{Colors.RED}[-] В локальных файлах совпадений нет.{Colors.END}")
        input(f"\n{Colors.YELLOW}Нажмите Enter для возврата...{Colors.END}")

    elif choice == '7':
        print(f"\n{Colors.CYAN}--- ГЕНЕРАТОР ОТЧЕТА ---{Colors.END}")
        fio = input("ФИО цели: ")
        id_tg = input("TG ID: ")
        # Сюда можно добавить любые поля из твоего обучения
        report_content = f"--- ОСНОВНОЙ ОТЧЕТ ---\nФИО: {fio}\nID: {id_tg}\n----------------------"
        print("\n" + report_content)
        if input("Сохранить отчет? (y/n): ").lower() == 'y':
            with open(f"reports/Dox_{id_tg}.txt", "w", encoding="utf-8") as f:
                f.write(report_content)
            print(f"[+] Отчет сохранен в папку reports.")
        input("\nEnter...")
        # === ДОПОЛНИТЕЛЬНЫЙ БЛОК (ПРОСТО ДОБАВИТЬ В КОНЕЦ) ===
        elif choice == '5':
            print(f"\n{Colors.MAGENTA}--- INFINITY INTELLIGENCE (БАЗЫ + ГОСУСЛУГИ) ---{Colors.END}")
            target = input(f"{Colors.CYAN}╰ Введите данные (ФИО/ТЕЛ/СНИЛС/НИК): {Colors.END}").lower()
            
            # Авто-поиск по всем твоим загруженным файлам
            dbs = [
                "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
                "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
                "Thailand.xls - Sheet 1.csv", "билайн юзеры.csv",
                "государственные услуги p3.csv"
            ]
            
            found_results = []
            for db in dbs:
                if os.path.exists(db):
                    try:
                        with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if target in line.lower():
                                    src = "ГОСУСЛУГИ" if "государственные" in db else db.split('.')[0].upper()
                                    out = f"[{src}] {line.strip()}"
                                    print(f"{Colors.GREEN}[+]{Colors.END} {out}")
                                    found_results.append(out)
                    except: pass

            # Полезные ссылки из твоих мануалов (Angel, Roxy, Reyzov)
            print(f"\n{Colors.YELLOW}--- OSINT ПОДСКАЗКИ ---{Colors.END}")
            print(f"📸 Фото: Яндекс 'intext:{target}'")
            print(f"🤖 Боты: @RedSearchBot | @visionerobot | @dosye_bot")
            print(f"🔑 Маскированные данные: VK Restore / Mail.ru Recovery")

            # Предложение сохранить отчет
            if found_results and input(f"\n{Colors.CYAN}Сохранить отчет? (y/n): {Colors.END}").lower() == 'y':
                with open(f"{REPORTS_DIR}/Final_Report_{int(time.time())}.txt", "w", encoding="utf-8") as rf:
                    rf.write(f"Результаты пробива по: {target}\n" + "\n".join(found_results))
                print(f"{Colors.GREEN}[+] Отчет готов в папке reports.{Colors.END}") 
        # === ОБНОВЛЕННЫЙ БЛОК: ПОИСК ПО ВСЕМ ЧАСТЯМ ГОСУСЛУГ ===
        elif choice == '5':
            print(f"\n{Colors.MAGENTA}--- INFINITY INTELLIGENCE (FULL GOSUSLUGI + BEELINE) ---{Colors.END}")
            target = input(f"{Colors.CYAN}╰ Введите данные (ФИО/ТЕЛ/СНИЛС): {Colors.END}").lower()
            
            # Авто-поиск по всем частям Госуслуг и другим базам
            dbs = [
                "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
                "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
                "Thailand.xls - Sheet 1.csv", "билайн юзеры.csv",
                "государственные услуги p1.csv", 
                "государственные услуги p2.csv", 
                "государственные услуги p3.csv"
            ]
            
            found_results = []
            print(f"[*] Сканирование всех архивов (p1, p2, p3)...")
            
            for db in dbs:
                if os.path.exists(db):
                    try:
                        with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if target in line.lower():
                                    # Маркировка источника
                                    if "государственные" in db:
                                        part = db.split(' ')[-1].split('.')[0] # Вытащит p1, p2 или p3
                                        src = f"ГОСУСЛУГИ {part.upper()}"
                                    else:
                                        src = db.split('.')[0].upper()
                                        
                                    out = f"[{src}] {line.strip()}"
                                    print(f"{Colors.GREEN}[+]{Colors.END} {out}")
                                    found_results.append(out)
                    except: 
                        continue

            # Доп. ресурсы из мануалов
            print(f"\n{Colors.YELLOW}--- OSINT ПОДСКАЗКИ ---{Colors.END}")
            print(f"📸 Фото: Яндекс 'intext:{target}'")
            print(f"🤖 Боты: @RedSearchBot | @visionerobot")
            print(f"🔑 Маскированные данные: VK Restore / Mail.ru Recovery")

            if found_results:
                if input(f"\n{Colors.CYAN}Сохранить полный отчет? (y/n): {Colors.END}").lower() == 'y':
                    filename = f"{REPORTS_DIR}/Full_Scan_{int(time.time())}.txt"
                    with open(filename, "w", encoding="utf-8") as rf:
                        rf.write(f"ГЛОБАЛЬНЫЙ ПОИСК: {target}\n" + "="*30 + "\n")
                        rf.write("\n".join(found_results))
                    print(f"{Colors.GREEN}[+] Данные из всех баз сохранены в {filename}{Colors.END}")
            else:
                print(f"\n{Colors.RED}[-] Совпадений не найдено ни в одной из баз.{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для выхода...{Colors.END}")
        # === ОБНОВЛЕННЫЙ БЛОК: ПОИСК ПО ВСЕМ ЧАСТЯМ ГОСУСЛУГ ===
        elif choice == '5':
            print(f"\n{Colors.MAGENTA}--- INFINITY INTELLIGENCE (FULL GOSUSLUGI + BEELINE) ---{Colors.END}")
            target = input(f"{Colors.CYAN}╰ Введите данные (ФИО/ТЕЛ/СНИЛС): {Colors.END}").lower()
            
            # Авто-поиск по всем частям Госуслуг и другим базам
            dbs = [
                "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
                "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
                "Thailand.xls - Sheet 1.csv", "билайн юзеры.csv",
                "государственные услуги p1.csv", 
                "государственные услуги p2.csv", 
                "государственные услуги p3.csv"
            ]
            
            found_results = []
            print(f"[*] Сканирование всех архивов (p1, p2, p3)...")
            
            for db in dbs:
                if os.path.exists(db):
                    try:
                        with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if target in line.lower():
                                    # Маркировка источника
                                    if "государственные" in db:
                                        part = db.split(' ')[-1].split('.')[0] # Вытащит p1, p2 или p3
                                        src = f"ГОСУСЛУГИ {part.upper()}"
                                    else:
                                        src = db.split('.')[0].upper()
                                        
                                    out = f"[{src}] {line.strip()}"
                                    print(f"{Colors.GREEN}[+]{Colors.END} {out}")
                                    found_results.append(out)
                    except: 
                        continue

            # Доп. ресурсы из мануалов
            print(f"\n{Colors.YELLOW}--- OSINT ПОДСКАЗКИ ---{Colors.END}")
            print(f"📸 Фото: Яндекс 'intext:{target}'")
            print(f"🤖 Боты: @RedSearchBot | @visionerobot")
            print(f"🔑 Маскированные данные: VK Restore / Mail.ru Recovery")

            if found_results:
                if input(f"\n{Colors.CYAN}Сохранить полный отчет? (y/n): {Colors.END}").lower() == 'y':
                    filename = f"{REPORTS_DIR}/Full_Scan_{int(time.time())}.txt"
                    with open(filename, "w", encoding="utf-8") as rf:
                        rf.write(f"ГЛОБАЛЬНЫЙ ПОИСК: {target}\n" + "="*30 + "\n")
                        rf.write("\n".join(found_results))
                    print(f"{Colors.GREEN}[+] Данные из всех баз сохранены в {filename}{Colors.END}")
            else:
                print(f"\n{Colors.RED}[-] Совпадений не найдено ни в одной из баз.{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для выхода...{Colors.END}")
        # === ОБНОВЛЕННЫЙ БЛОК: ПОИСК ПО ВСЕМ ЧАСТЯМ ГОСУСЛУГ ===
        elif choice == '5':
            print(f"\n{Colors.MAGENTA}--- INFINITY INTELLIGENCE (FULL GOSUSLUGI + BEELINE) ---{Colors.END}")
            target = input(f"{Colors.CYAN}╰ Введите данные (ФИО/ТЕЛ/СНИЛС): {Colors.END}").lower()
            
            # Авто-поиск по всем частям Госуслуг и другим базам
            dbs = [
                "Zambia.xls - Sheet 1.csv", "Switzerland.xls - Sheet 1.csv",
                "USA_ExportErrors.xls - Sheet 1.csv", "Taiwan.xls - Sheet 1.csv",
                "Thailand.xls - Sheet 1.csv", "билайн юзеры.csv",
                "государственные услуги p1.csv", 
                "государственные услуги p2.csv", 
                "государственные услуги p3.csv"
            ]
            
            found_results = []
            print(f"[*] Сканирование всех архивов (p1, p2, p3)...")
            
            for db in dbs:
                if os.path.exists(db):
                    try:
                        with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if target in line.lower():
                                    # Маркировка источника
                                    if "государственные" in db:
                                        part = db.split(' ')[-1].split('.')[0] # Вытащит p1, p2 или p3
                                        src = f"ГОСУСЛУГИ {part.upper()}"
                                    else:
                                        src = db.split('.')[0].upper()
                                        
                                    out = f"[{src}] {line.strip()}"
                                    print(f"{Colors.GREEN}[+]{Colors.END} {out}")
                                    found_results.append(out)
                    except: 
                        continue

            # Доп. ресурсы из мануалов
            print(f"\n{Colors.YELLOW}--- OSINT ПОДСКАЗКИ ---{Colors.END}")
            print(f"📸 Фото: Яндекс 'intext:{target}'")
            print(f"🤖 Боты: @RedSearchBot | @visionerobot")
            print(f"🔑 Маскированные данные: VK Restore / Mail.ru Recovery")

            if found_results:
                if input(f"\n{Colors.CYAN}Сохранить полный отчет? (y/n): {Colors.END}").lower() == 'y':
                    filename = f"{REPORTS_DIR}/Full_Scan_{int(time.time())}.txt"
                    with open(filename, "w", encoding="utf-8") as rf:
                        rf.write(f"ГЛОБАЛЬНЫЙ ПОИСК: {target}\n" + "="*30 + "\n")
                        rf.write("\n".join(found_results))
                    print(f"{Colors.GREEN}[+] Данные из всех баз сохранены в {filename}{Colors.END}")
            else:
                print(f"\n{Colors.RED}[-] Совпадений не найдено ни в одной из баз.{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для выхода...{Colors.END}")
        # === НОВЫЙ БЛОК: ДЕАНОН INSTAGRAM (МЕТОДЫ ИЗ МАНУАЛА) ===
        elif choice == '10':
            print(f"\n{Colors.MAGENTA}--- OSINT: РАЗВЕДКА INSTAGRAM ---{Colors.END}")
            insta_nick = input(f"{Colors.CYAN}╰ Введите Nickname или ссылку: {Colors.END}").replace('@', '')
            
            print(f"\n{Colors.YELLOW}[!] РЕКОМЕНДУЕМЫЕ ИНСТРУМЕНТЫ (ИЗ МАНУАЛА):{Colors.END}")
            
            # Инструменты из твоего текстового файла
            tools = {
                "🔍 SearchMy": "Поиск профиля по всей базе сервиса.",
                "🖼️ Instadp": "Получение аватарки в полном размере и HD качестве.",
                "👥 FindClone": "Поиск родственников или других аккаунтов по фото профиля.",
                "💻 Av3 (Chrome)": "Расширение для глубокого сбора инфы об аккаунте.",
                "🤖 Maigret (Бот)": "Поиск других соцсетей цели по этому же никнейму."
            }
            
            for tool, desc in tools.items():
                print(f"{Colors.WHITE}{tool}{Colors.END} — {desc}")
            
            print(f"\n{Colors.CYAN}--- БЫСТРЫЕ ССЫЛКИ ДЛЯ {insta_nick} ---{Colors.END}")
            print(f"🔗 Профиль: https://instagram.com/{insta_nick}")
            print(f"🔗 Ник в других сетях: https://whatsmyname.app/ (введи {insta_nick})")
            print(f"🤖 Telegram бот: @Maigret_bot")
            
            # Локальная проверка (вдруг ник или почта инсты есть в Госуслугах или Билайне)
            print(f"\n[*] Проверка ника {insta_nick} в локальных базах...")
            found = False
            for db in DB_FILES:
                if os.path.exists(db):
                    try:
                        with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if insta_nick in line.lower():
                                    print(f"{Colors.GREEN}[+] Найдено совпадение [{db}]: {line.strip()}{Colors.END}")
                                    found = True
                    except: pass
            
            if not found:
                print(f"{Colors.RED}[-] В локальных базах прямых упоминаний ника не найдено.{Colors.END}")

            input(f"\n{Colors.YELLOW}Нажмите Enter для возврата...{Colors.END}")
        # === НОВЫЙ БЛОК: ПОИСК ПО EMAIL (ИЗ МАНУАЛА) ===
        elif choice == '11':
            print(f"\n{Colors.CYAN}--- OSINT: РАЗВЕДКА ПО ПОЧТЕ (EMAIL) ---{Colors.END}")
            email_target = input(f"{Colors.YELLOW}╰ Введите Email цели: {Colors.END}").lower().strip()
            
            print(f"\n{Colors.MAGENTA}--- РЕКОМЕНДУЕМЫЕ БОТЫ (ИЗ МАНУАЛА) ---{Colors.END}")
            mail_bots = [
                ("@mailExistsBot", "Покажет, в каких сервисах зарегистрирована почта."),
                ("@last4mailbot", "Ищет в ОК и Сбере (помогает собрать номер по частям)."),
                ("@GetGmail_bot", "Выдает основную информацию о владельце Gmail."),
                ("@EmailPhoneOSINT_bot", "Ищет прямую привязку почты к номеру телефона.")
            ]
            
            for bot_name, desc in mail_bots:
                print(f"{Colors.WHITE}{bot_name}{Colors.END} — {desc}")
            
            # Автоматический пробив по локальным архивам
            print(f"\n[*] Проверка почты {email_target} в локальных базах...")
            found_in_db = False
            
            # Список баз для поиска
            for db in DB_FILES:
                if os.path.exists(db):
                    try:
                        with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if email_target in line.lower():
                                    src = "ГОСУСЛУГИ" if "государственные" in db else db.split('.')[0].upper()
                                    print(f"{Colors.GREEN}[+] НАЙДЕНО [{src}]: {line.strip()}{Colors.END}")
                                    found_in_db = True
                    except:
                        continue
            
            if not found_in_db:
                print(f"{Colors.RED}[-] В локальных файлах (Госуслуги/Beeline) почта не найдена.{Colors.END}")
            
            # Быстрая ссылка на поиск в Google
            print(f"\n{Colors.BLUE}--- ГЛОБАЛЬНЫЙ ПОИСК ---{Colors.END}")
            print(f"🔗 Google Dork: https://www.google.com/search?q=\"{email_target}\"")
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для возврата...{Colors.END}")
        # === НОВЫЙ БЛОК: ЭКСПЕРТНЫЙ OSINT (MANUAL 3 LVL + HESONBY) ===
        elif choice == '12':
            print(f"\n{Colors.RED}--- EXPERT OSINT & DOXING TOOLS (LVL 3) ---{Colors.END}")
            print(f"{Colors.WHITE}Выберите направление разведки:{Colors.END}")
            print(" 1 - Геолокация по фото (анализ фона)")
            print(" 2 - Работа с IP и Инфраструктурой")
            print(" 3 - Шаблон оформления DOX-отчета")
            
            sub_choice = input(f"\n{Colors.CYAN}╰ Ваш выбор: {Colors.END}")

            if sub_choice == '1':
                print(f"\n{Colors.YELLOW}[!] АНАЛИЗ ИЗОБРАЖЕНИЙ:{Colors.END}")
                print("• FindClone / Search4Faces — поиск лиц.")
                print("• Тщательно проверь фон: номера машин, вывески, чеки, отражения в окнах.")
                print("• Метаданные: используй @ExifCleanerBot для поиска координат в файле.")
                
            elif sub_choice == '2':
                print(f"\n{Colors.BLUE}[!] IP & NETWORK:{Colors.END}")
                print("• Идентификация провайдера (ISP) и типа соединения (VPN/Proxy).")
                print("• Ресурсы: Whois.com, DNSChecker.org, IP-score.com.")
                print("• Поиск по IP в базах сливов на наличие ника/почты.")
                
            elif sub_choice == '3':
                print(f"\n{Colors.WHITE}[!] ШАБЛОН ОТЧЕТА (ИЗ МАНУАЛА):{Colors.END}")
                template = """
====================
* Personal Information:
Full Name: 
Phone: 
DOB: 
Email: 
Picture/Alias: 
* Location:
Address/Zip/City: 
* IP Information:
IP/ISP/VPN: 
* Social Media:
VK/Inst/Steam: 
===================="""
                print(Colorate.Horizontal(Colors.green_to_blue, template))

            input(f"\n{Colors.YELLOW}Нажмите Enter для возврата...{Colors.END}")
        # === НОВЫЙ БЛОК: ЦИФРОВЫЕ СЛЕДЫ И АРХИВЫ (OSINT PACK) ===
        elif choice == '13':
            print(f"\n{Colors.GREEN}--- OSINT: ЦИФРОВЫЕ СЛЕДЫ И ГЕО-РАЗВЕДКА ---{Colors.END}")
            print(f"{Colors.WHITE}Доступные инструменты из пака:{Colors.END}")
            
            # Список из твоего файла osint pack.txt
            archive_tools = [
                ("📍 SNRadar", "Карта фотографий VK (ищет фото по координатам и времени)."),
                ("📂 InInterests", "Архив страниц VK. Помогает найти данные удалённых профилей."),
                ("🆔 RegVK", "Узнать оригинальный ID и дату регистрации по короткой ссылке."),
                ("🛡️ Tor Exit Nodes", "Проверка, связан ли IP с выходными узлами Tor."),
                ("🤖 Stoned Eyes", "Комплексный пробив (Авто, ФИО, Фото).")
            ]
            
            for name, desc in archive_tools:
                print(f"{Colors.CYAN}{name}{Colors.END} — {desc}")
            
            print(f"\n{Colors.YELLOW}--- ПРЯМЫЕ ССЫЛКИ ДЛЯ РАБОТЫ ---{Colors.END}")
            print(f"🔗 Карта фото: https://snradar.azurewebsites.net")
            print(f"🔗 Архив VK: http://ininterests.com/")
            print(f"🔗 Узнать ID: https://regvk.com/id/")
            
            # Предложим быстрый поиск по ID, если пользователь его уже нашел
            target_id = input(f"\n{Colors.WHITE}Введите найденный ID для поиска в локальных базах (или Enter): {Colors.END}")
            if target_id:
                print(f"[*] Проверка ID {target_id} по всем базам...")
                found = False
                for db in DB_FILES:
                    if os.path.exists(db):
                        try:
                            with open(db, 'r', encoding='utf-8', errors='ignore') as f:
                                for line in f:
                                    if target_id in line:
                                        print(f"{Colors.GREEN}[+] Найдено в {db}: {line.strip()}{Colors.END}")
                                        found = True
                        except: pass
                if not found:
                    print(f"{Colors.RED}[-][-] Совпадений по ID не найдено.{Colors.END}")

            input(f"\n{Colors.YELLOW}Нажмите Enter для возврата...{Colors.END}")
