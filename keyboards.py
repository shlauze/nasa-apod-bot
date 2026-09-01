# pyrefly: ignore [missing-import]
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from locales import format_date_localized, get_text


def get_main_menu_inline(lang: str = "ru") -> InlineKeyboardMarkup:
    """Главное меню бота с локализацией"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text("btn_today", lang), callback_data="menu:today"),
                InlineKeyboardButton(text=get_text("btn_random", lang), callback_data="menu:random"),
            ],
            [
                InlineKeyboardButton(text=get_text("btn_date", lang), callback_data="menu:date"),
                InlineKeyboardButton(text=get_text("btn_birthday", lang), callback_data="menu:birthday"),
            ],
            [
                InlineKeyboardButton(text=get_text("btn_language", lang), callback_data="menu:language"),
                InlineKeyboardButton(text=get_text("btn_about", lang), callback_data="menu:about"),
            ],
        ]
    )


def get_language_inline(current_lang: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    ru_label = "🇷🇺 Русский" + (" ✅" if current_lang == "ru" else "")
    en_label = "🇬🇧 English" + (" ✅" if current_lang == "en" else "")

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=ru_label, callback_data="lang:ru"),
                InlineKeyboardButton(text=en_label, callback_data="lang:en"),
            ],
            [
                InlineKeyboardButton(text=get_text("btn_back", current_lang), callback_data="menu:home"),
            ],
        ]
    )


def get_cancel_inline(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка отмены для выхода из режима ввода"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="menu:home")
            ]
        ]
    )


def get_apod_actions_inline(
    nasa_url: str,
    hd_url: str | None = None,
    is_random: bool = False,
    is_birthday: bool = False,
    lang: str = "ru",
) -> InlineKeyboardMarkup:
    """Интерактивные кнопки под карточкой APOD"""
    keyboard = []

    first_row = []
    if nasa_url:
        first_row.append(InlineKeyboardButton(text=get_text("btn_nasa_page", lang), url=nasa_url))
    if hd_url and hd_url != nasa_url:
        first_row.append(InlineKeyboardButton(text=get_text("btn_hd_quality", lang), url=hd_url))

    if first_row:
        keyboard.append(first_row)

    second_row = []
    if is_random:
        second_row.append(InlineKeyboardButton(text=get_text("btn_another_random", lang), callback_data="menu:random"))
    elif is_birthday:
        second_row.append(InlineKeyboardButton(text=get_text("btn_another_birthday", lang), callback_data="menu:birthday"))
    else:
        second_row.append(InlineKeyboardButton(text=get_text("btn_another_date", lang), callback_data="menu:date"))

    second_row.append(InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="menu:home"))
    keyboard.append(second_row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_pre1995_birthday_inline(next_birthday_iso: str, lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопки для дней рождения до 16.06.1995"""
    formatted_target = format_date_localized(next_birthday_iso, lang)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text("btn_pre1995_bday", lang, date=formatted_target),
                    callback_data=f"date:{next_birthday_iso}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text("btn_first_apod", lang),
                    callback_data="date:1995-06-16",
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text("btn_main_menu", lang),
                    callback_data="menu:home",
                )
            ],
        ]
    )
