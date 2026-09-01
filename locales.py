from datetime import datetime

STRINGS = {
    "ru": {
        # Menu buttons
        "btn_today": "🌌 APOD за сегодня",
        "btn_random": "🎲 Случайный снимок",
        "btn_date": "📅 Выбрать дату",
        "btn_birthday": "🎂 APOD в день рождения",
        "btn_language": "🌐 Язык / Language",
        "btn_about": "ℹ️ О проекте",
        "btn_cancel": "❌ Отмена / В главное меню",
        "btn_nasa_page": "🔗 Страница NASA",
        "btn_hd_quality": "🔍 HD качество",
        "btn_another_random": "🎲 Ещё случайный",
        "btn_another_birthday": "🎂 Другой день рождения",
        "btn_another_date": "📅 Другая дата",
        "btn_main_menu": "🏠 Главное меню",
        "btn_pre1995_bday": "🎂 Снимок в первый доступный год ({date})",
        "btn_first_apod": "🌟 Первый APOD в истории (16.06.1995)",
        "btn_back": "⬅️ Назад",

        # Start / Menu
        "welcome": (
            "🌌 <b>Добро пожаловать в NASA APOD Bot!</b>\n\n"
            "Каждый день NASA публикует уникальный снимок или видео Вселенной "
            "с описанием от профессиональных астрономов (<b>Astronomy Picture of the Day</b>).\n\n"
            "✨ <b>Что вы хотите посмотреть?</b>\n"
            "Выберите действие в меню ниже или отправьте дату (например, <code>16.06.1995</code>)."
        ),
        "main_menu_title": "🌌 <b>Главное меню NASA APOD Bot</b>\n\nВыберите интересующий раздел:",

        # Language selection
        "choose_language": "🌐 <b>Выберите язык интерфейса / Choose your language:</b>",
        "language_changed": "✅ Язык успешно изменён на <b>Русский 🇷🇺</b>!",

        # Birthday
        "birthday_prompt": (
            "🎂 <b>Узнай, какой космический снимок NASA опубликовала в день твоего рождения!</b>\n\n"
            "📅 Отправь дату своего рождения в формате:\n"
            "<code>ДД.ММ.ГГГГ</code> (например, <code>14.03.2006</code>)\n\n"
            "<i>Если передумал — нажми кнопку отмены.</i>"
        ),
        "birthday_header": "🎂 <b>В день твоего рождения ({date}) NASA опубликовала:</b>\n\n",
        "birthday_future": "🚀 <b>Эта дата из будущего!</b>\nПожалуйста, введите настоящую дату вашего рождения:",
        "birthday_pre1995": (
            "✨ <b>Вы родились {user_date}</b> — до того, как NASA запустила проект APOD (16 июня 1995 г.).\n\n"
            "Но мы можем посмотреть снимок в ваш первый доступный день рождения в архиве ({target_date}) "
            "или самый первый снимок в истории APOD!"
        ),

        # Select date
        "date_prompt": (
            "📅 <b>Поиск снимка по дате</b>\n\n"
            "Архив доступен с <b>16 июня 1995 года</b> по сегодняшний день.\n\n"
            "Отправь дату в формате:\n"
            "• <code>16.06.1995</code>\n"
            "• <code>2020-01-01</code>"
        ),
        "invalid_date": (
            "❌ <b>Не удалось распознать дату.</b>\n\n"
            "Пожалуйста, используйте формат <code>ДД.ММ.ГГГГ</code> (например, <code>16.06.1995</code>) "
            "или <code>ГГГГ-ММ-ДД</code>."
        ),
        "date_too_early": (
            "❌ <b>Эта дата слишком ранняя.</b>\n\n"
            "Первый выпуск APOD в архиве NASA появился <b>16 июня 1995 года</b>."
        ),
        "date_future": (
            "🚀 <b>Эта дата находится в будущем.</b>\n\n"
            "NASA ещё не опубликовала космический снимок за этот день."
        ),

        # Common
        "searching": "🔭 <i>Ищу снимок в архивах NASA...</i>",
        "not_found": "❌ Для этой даты снимок не найден в архиве.",
        "api_error": "⚠️ Произошла ошибка при обращении к NASA API.\nПопробуйте позже.",
        "canceled": "✅ Действие отменено.",
        "unknown_input": (
            "👋 Я не распознал команду или дату.\n\n"
            "Отправьте дату (например, <code>16.06.1995</code>) или выберите действие в меню:"
        ),
        "description_label": "📝 <b>Описание:</b>",
        "video_label": "🎥 <b>Видео:</b>",
        "watch_video": "Смотреть на источнике",
        "random_header": "🎲 <b>Случайный снимок из архива ({date}):</b>\n\n",
        "date_header": "📅 <b>{date}</b>\n\n",

        # About
        "about_text": (
            "ℹ️ <b>О проекте NASA Astronomy Picture of the Day (APOD)</b>\n\n"
            "🌌 <b>APOD</b> — один из старейших и известнейших научно-популярных проектов NASA, "
            "созданный астрономами Робертом Немироффом и Джерри Боннеллом <b>16 июня 1995 года</b>.\n\n"
            "Каждый день публикуется новый снимок нашей Вселенной с кратким пояснением от профессиональных астрономов.\n\n"
            "🔭 <b>Функции бота:</b>\n"
            "• 🌌 <b>Сегодня</b> — свежий снимок дня\n"
            "• 🎲 <b>Случайный</b> — исследуйте более 10 000 явлений космоса\n"
            "• 📅 <b>По дате</b> — любой день с 16 июня 1995 года\n"
            "• 🎂 <b>День рождения</b> — какой снимок был опубликован в день твоего рождения\n"
            "• 🌐 <b>Язык</b> — переключение RU / EN\n\n"
            "🔗 Официальный сайт: <a href=\"https://apod.nasa.gov/apod/\">apod.nasa.gov</a>"
        ),
    },

    "en": {
        # Menu buttons
        "btn_today": "🌌 Today's APOD",
        "btn_random": "🎲 Random Picture",
        "btn_date": "📅 Select Date",
        "btn_birthday": "🎂 Birthday APOD",
        "btn_language": "🌐 Language / Язык",
        "btn_about": "ℹ️ About APOD",
        "btn_cancel": "❌ Cancel / Main Menu",
        "btn_nasa_page": "🔗 NASA Page",
        "btn_hd_quality": "🔍 HD Quality",
        "btn_another_random": "🎲 Another Random",
        "btn_another_birthday": "🎂 Another Birthday",
        "btn_another_date": "📅 Another Date",
        "btn_main_menu": "🏠 Main Menu",
        "btn_pre1995_bday": "🎂 First available year ({date})",
        "btn_first_apod": "🌟 First APOD in history (June 16, 1995)",
        "btn_back": "⬅️ Back",

        # Start / Menu
        "welcome": (
            "🌌 <b>Welcome to NASA APOD Bot!</b>\n\n"
            "Every day NASA features a different astronomy picture or video of our fascinating Universe, "
            "along with a brief explanation written by a professional astronomer (<b>Astronomy Picture of the Day</b>).\n\n"
            "✨ <b>What would you like to explore?</b>\n"
            "Select an option from the menu below or send a date directly (e.g., <code>1995-06-16</code> or <code>16.06.1995</code>)."
        ),
        "main_menu_title": "🌌 <b>NASA APOD Bot Main Menu</b>\n\nChoose an option:",

        # Language selection
        "choose_language": "🌐 <b>Choose your language / Выберите язык интерфейса:</b>",
        "language_changed": "✅ Language successfully switched to <b>English 🇬🇧</b>!",

        # Birthday
        "birthday_prompt": (
            "🎂 <b>Discover what cosmic event NASA published on your birthday!</b>\n\n"
            "📅 Send your birth date in format:\n"
            "<code>DD.MM.YYYY</code> or <code>YYYY-MM-DD</code> (e.g. <code>14.03.2006</code>)\n\n"
            "<i>Click cancel if you change your mind.</i>"
        ),
        "birthday_header": "🎂 <b>On your birthday ({date}) NASA published:</b>\n\n",
        "birthday_future": "🚀 <b>This date is in the future!</b>\nPlease enter your actual date of birth:",
        "birthday_pre1995": (
            "✨ <b>You were born on {user_date}</b> — before NASA started the APOD project (June 16, 1995).\n\n"
            "However, we can look at the picture on your first available birthday in the archive ({target_date}) "
            "or check out the very first APOD in history!"
        ),

        # Select date
        "date_prompt": (
            "📅 <b>Search APOD by Date</b>\n\n"
            "Archive is available from <b>June 16, 1995</b> to today.\n\n"
            "Send a date in format:\n"
            "• <code>16.06.1995</code>\n"
            "• <code>1995-06-16</code>"
        ),
        "invalid_date": (
            "❌ <b>Could not recognize the date format.</b>\n\n"
            "Please use format <code>DD.MM.YYYY</code> (e.g., <code>16.06.1995</code>) "
            "or <code>YYYY-MM-DD</code>."
        ),
        "date_too_early": (
            "❌ <b>This date is too early.</b>\n\n"
            "The very first APOD was published on <b>June 16, 1995</b>."
        ),
        "date_future": (
            "🚀 <b>This date is in the future.</b>\n\n"
            "NASA has not published a picture for this day yet."
        ),

        # Common
        "searching": "🔭 <i>Searching NASA archives...</i>",
        "not_found": "❌ No APOD found for this date in NASA archives.",
        "api_error": "⚠️ An error occurred while contacting NASA API.\nPlease try again later.",
        "canceled": "✅ Action canceled.",
        "unknown_input": (
            "👋 Command or date not recognized.\n\n"
            "Send a date (e.g. <code>16.06.1995</code>) or choose an option from the menu:"
        ),
        "description_label": "📝 <b>Explanation:</b>",
        "video_label": "🎥 <b>Video:</b>",
        "watch_video": "Watch on source",
        "random_header": "🎲 <b>Random picture from archive ({date}):</b>\n\n",
        "date_header": "📅 <b>{date}</b>\n\n",

        # About
        "about_text": (
            "ℹ️ <b>About NASA Astronomy Picture of the Day (APOD)</b>\n\n"
            "🌌 <b>APOD</b> is one of NASA's most popular science communication projects, "
            "created by astronomers Robert Nemiroff and Jerry Bonnell on <b>June 16, 1995</b>.\n\n"
            "Every day a new image or video of our Universe is published alongside a professional explanation.\n\n"
            "🔭 <b>Bot features:</b>\n"
            "• 🌌 <b>Today</b> — today's fresh cosmic picture\n"
            "• 🎲 <b>Random</b> — explore 10,000+ cosmic phenomena\n"
            "• 📅 <b>By Date</b> — any day since June 16, 1995\n"
            "• 🎂 <b>Birthday</b> — what cosmic photo was featured on the day you were born\n"
            "• 🌐 <b>Language</b> — switch between RU / EN\n\n"
            "🔗 Official website: <a href=\"https://apod.nasa.gov/apod/\">apod.nasa.gov</a>"
        ),
    },
}


def get_text(key: str, lang: str = "ru", **kwargs) -> str:
    """Возвращает строку на нужном языке с подстановкой параметров"""
    lang_dict = STRINGS.get(lang, STRINGS["ru"])
    template = lang_dict.get(key, STRINGS["ru"].get(key, f"[{key}]"))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def format_date_localized(apod_date_str: str, lang: str = "ru") -> str:
    """Форматирует дату YYYY-MM-DD на русском или английском языке"""
    d = datetime.strptime(apod_date_str, "%Y-%m-%d")
    if lang == "en":
        months_en = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        return f"{months_en[d.month - 1]} {d.day}, {d.year}"

    months_ru = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    ]
    return f"{d.day} {months_ru[d.month - 1]} {d.year} года"
