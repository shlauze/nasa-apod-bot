import asyncio
import html
import logging
import os
import random
from datetime import date, datetime

# pyrefly: ignore [missing-import]
from aiohttp import web

# pyrefly: ignore [missing-import]
from aiogram import Bot, Dispatcher, F
# pyrefly: ignore [missing-import]
from aiogram.client.default import DefaultBotProperties
# pyrefly: ignore [missing-import]
from aiogram.enums import ParseMode
# pyrefly: ignore [missing-import]
from aiogram.filters import Command, StateFilter
# pyrefly: ignore [missing-import]
from aiogram.fsm.context import FSMContext
# pyrefly: ignore [missing-import]
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    Message,
)

from config import BOT_TOKEN
from keyboards import (
    get_apod_actions_inline,
    get_cancel_inline,
    get_language_inline,
    get_main_menu_inline,
    get_pre1995_birthday_inline,
)
from locales import format_date_localized, get_text
from nasa import MIN_DATE, get_apod
from states import ApodStates
from storage import get_user_language, set_user_language

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

dp = Dispatcher()


def parse_user_date(text: str) -> date | None:
    """Парсит дату из различных распространенных форматов"""
    formats = [
        "%d.%m.%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d %m %Y",
    ]
    cleaned = text.strip()
    for fmt in formats:
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            pass
    return None


async def set_bot_commands(bot: Bot):
    """Регистрирует список команд в Telegram"""
    commands = [
        BotCommand(command="start", description="🏠 Главное меню / Main menu"),
        BotCommand(command="today", description="🌌 APOD за сегодня / Today"),
        BotCommand(command="random", description="🎲 Случайный APOD / Random"),
        BotCommand(command="birthday", description="🎂 APOD в день рождения / Birthday"),
        BotCommand(command="date", description="📅 Выбрать дату / Select date"),
        BotCommand(command="language", description="🌐 Язык / Language"),
        BotCommand(command="about", description="ℹ️ О проекте / About"),
        BotCommand(command="cancel", description="❌ Отмена / Cancel"),
    ]
    await bot.set_my_commands(commands)


# --------------------------- ОБРАБОТЧИКИ КОМАНД --------------------------- #


@dp.message(Command("start"))
async def start_cmd_handler(message: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    welcome_text = get_text("welcome", lang)
    await message.answer(welcome_text, reply_markup=get_main_menu_inline(lang))


@dp.message(Command("language", "lang"))
async def language_cmd_handler(message: Message):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    await message.answer(
        get_text("choose_language", lang),
        reply_markup=get_language_inline(lang),
    )


@dp.message(Command("cancel"))
async def cancel_cmd_handler(message: Message, state: FSMContext):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer(
            get_text("canceled", lang),
            reply_markup=get_main_menu_inline(lang),
        )
    else:
        await message.answer(
            get_text("main_menu_title", lang),
            reply_markup=get_main_menu_inline(lang),
        )


@dp.message(Command("today"))
async def today_cmd_handler(message: Message, state: FSMContext):
    await state.clear()
    await send_apod(message, date.today())


@dp.message(Command("random"))
async def random_cmd_handler(message: Message, state: FSMContext):
    await state.clear()
    today = date.today()
    random_ordinal = random.randint(MIN_DATE.toordinal(), today.toordinal())
    random_date = date.fromordinal(random_ordinal)
    await send_apod(message, random_date, is_random=True)


@dp.message(Command("birthday"))
async def birthday_cmd_handler(message: Message, state: FSMContext):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    await state.set_state(ApodStates.waiting_for_birthday)
    await message.answer(
        get_text("birthday_prompt", lang),
        reply_markup=get_cancel_inline(lang),
    )


@dp.message(Command("date"))
async def date_cmd_handler(message: Message, state: FSMContext):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    await state.set_state(ApodStates.waiting_for_date)
    await message.answer(
        get_text("date_prompt", lang),
        reply_markup=get_cancel_inline(lang),
    )


@dp.message(Command("about"))
async def about_cmd_handler(message: Message):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    await message.answer(
        get_text("about_text", lang),
        reply_markup=get_main_menu_inline(lang),
    )


# --------------------------- ОБРАБОТЧИКИ CALLBACK КНОПОК --------------------------- #


@dp.callback_query(F.data.startswith("lang:"))
async def language_callback_handler(call: CallbackQuery):
    new_lang = call.data.split(":")[1]
    user_id = call.from_user.id
    set_user_language(user_id, new_lang)
    await call.answer(
        "🇷🇺 Выбран русский язык" if new_lang == "ru" else "🇬🇧 English selected",
        show_alert=False,
    )

    confirm_text = (
        get_text("language_changed", new_lang) + "\n\n" + get_text("main_menu_title", new_lang)
    )
    try:
        await call.message.edit_text(confirm_text, reply_markup=get_main_menu_inline(new_lang))
    except Exception:
        await call.message.answer(confirm_text, reply_markup=get_main_menu_inline(new_lang))


@dp.callback_query(F.data.startswith("menu:"))
async def menu_callbacks_handler(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    lang = get_user_language(
        call.from_user.id,
        call.from_user.language_code,
    )
    await call.answer()

    if action == "home":
        await state.clear()
        title_text = get_text("main_menu_title", lang)
        try:
            await call.message.edit_text(title_text, reply_markup=get_main_menu_inline(lang))
        except Exception:
            await call.message.answer(title_text, reply_markup=get_main_menu_inline(lang))

    elif action == "language":
        try:
            await call.message.edit_text(
                get_text("choose_language", lang),
                reply_markup=get_language_inline(lang),
            )
        except Exception:
            await call.message.answer(
                get_text("choose_language", lang),
                reply_markup=get_language_inline(lang),
            )

    elif action == "today":
        await state.clear()
        await send_apod(call.message, date.today(), user_id=call.from_user.id)

    elif action == "random":
        await state.clear()
        today = date.today()
        random_ordinal = random.randint(MIN_DATE.toordinal(), today.toordinal())
        random_date = date.fromordinal(random_ordinal)
        await send_apod(call.message, random_date, is_random=True, user_id=call.from_user.id)

    elif action == "birthday":
        await state.set_state(ApodStates.waiting_for_birthday)
        prompt_text = get_text("birthday_prompt", lang)
        try:
            await call.message.edit_text(prompt_text, reply_markup=get_cancel_inline(lang))
        except Exception:
            await call.message.answer(prompt_text, reply_markup=get_cancel_inline(lang))

    elif action == "date":
        await state.set_state(ApodStates.waiting_for_date)
        prompt_text = get_text("date_prompt", lang)
        try:
            await call.message.edit_text(prompt_text, reply_markup=get_cancel_inline(lang))
        except Exception:
            await call.message.answer(prompt_text, reply_markup=get_cancel_inline(lang))

    elif action == "about":
        about_text = get_text("about_text", lang)
        try:
            await call.message.edit_text(about_text, reply_markup=get_main_menu_inline(lang))
        except Exception:
            await call.message.answer(about_text, reply_markup=get_main_menu_inline(lang))


@dp.callback_query(F.data.startswith("date:"))
async def callback_date_handler(call: CallbackQuery, state: FSMContext):
    date_str = call.data.split(":")[1]
    lang = get_user_language(
        call.from_user.id,
        call.from_user.language_code,
    )
    await call.answer()
    try:
        apod_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        await send_apod(call.message, apod_date, user_id=call.from_user.id)
    except Exception as e:
        logger.error("Error parsing callback date: %s", e)
        await call.message.answer(get_text("api_error", lang))


# --------------------------- FSM И ТЕКСТОВЫЕ ОБРАБОТЧИКИ --------------------------- #


@dp.message(StateFilter(ApodStates.waiting_for_birthday))
async def birthday_input_handler(message: Message, state: FSMContext):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    user_date = parse_user_date(message.text)
    if user_date is None:
        await message.answer(
            get_text("invalid_date", lang),
            reply_markup=get_cancel_inline(lang),
        )
        return

    today = date.today()
    if user_date > today:
        await message.answer(
            get_text("birthday_future", lang),
            reply_markup=get_cancel_inline(lang),
        )
        return

    await state.clear()

    # Если человек родился до первого выпуска APOD (16 июня 1995)
    if user_date < MIN_DATE:
        next_available_year = (
            1995
            if (user_date.month > 6 or (user_date.month == 6 and user_date.day >= 16))
            else 1996
        )
        target_day = 28 if (user_date.month == 2 and user_date.day == 29) else user_date.day
        first_available_bday = date(next_available_year, user_date.month, target_day)

        user_date_formatted = format_date_localized(user_date.isoformat(), lang)
        target_date_formatted = format_date_localized(first_available_bday.isoformat(), lang)

        msg_text = get_text(
            "birthday_pre1995",
            lang,
            user_date=user_date_formatted,
            target_date=target_date_formatted,
        )
        await message.answer(
            msg_text,
            reply_markup=get_pre1995_birthday_inline(first_available_bday.isoformat(), lang),
        )
        return

    # Если дата в рамках архива
    await send_apod(message, user_date, is_birthday=True)


@dp.message(StateFilter(ApodStates.waiting_for_date))
async def date_input_handler(message: Message, state: FSMContext):
    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    user_date = parse_user_date(message.text)
    if user_date is None:
        await message.answer(
            get_text("invalid_date", lang),
            reply_markup=get_cancel_inline(lang),
        )
        return

    await state.clear()
    await send_apod(message, user_date)


@dp.message(F.text)
async def fallback_text_handler(message: Message, state: FSMContext):
    """Обрабатывает ввод даты пользователем вне состояний FSM"""
    user_date = parse_user_date(message.text)
    if user_date is not None:
        await state.clear()
        await send_apod(message, user_date)
        return

    lang = get_user_language(
        message.from_user.id,
        message.from_user.language_code,
    )
    await message.answer(
        get_text("unknown_input", lang),
        reply_markup=get_main_menu_inline(lang),
    )


# --------------------------- ОСНОВНАЯ ФУНКЦИЯ ОТПРАВКИ APOD --------------------------- #


async def send_apod(
    message: Message,
    apod_date: date,
    is_random: bool = False,
    is_birthday: bool = False,
    user_id: int | None = None,
):
    target_user_id = user_id or (message.from_user.id if message.from_user else 0)
    lang = get_user_language(target_user_id)

    today = date.today()
    if apod_date < MIN_DATE:
        await message.answer(
            get_text("date_too_early", lang),
            reply_markup=get_main_menu_inline(lang),
        )
        return
    if apod_date > today:
        await message.answer(
            get_text("date_future", lang),
            reply_markup=get_main_menu_inline(lang),
        )
        return

    status_msg = await message.answer(get_text("searching", lang))

    try:
        data = await get_apod(apod_date)
    except ValueError:
        await status_msg.edit_text(get_text("not_found", lang))
        return
    except RuntimeError as e:
        logger.warning("NASA API error: %s", e)
        await status_msg.edit_text(f"⚠️ {e}")
        return
    except Exception as error:
        logger.exception("Unexpected error fetching APOD: %s", error)
        await status_msg.edit_text(get_text("api_error", lang))
        return

    try:
        await status_msg.delete()
    except Exception:
        pass

    title = html.escape(data.get("title", "Untitled"))
    explanation = html.escape(data.get("explanation", "No description available."))
    apod_url = data.get("url", "")
    hd_url = data.get("hdurl")
    media_type = data.get("media_type", "image")
    formatted_date = format_date_localized(data["date"], lang)

    if is_birthday:
        header = get_text("birthday_header", lang, date=formatted_date)
    elif is_random:
        header = get_text("random_header", lang, date=formatted_date)
    else:
        header = get_text("date_header", lang, date=formatted_date)

    desc_label = get_text("description_label", lang)
    caption_full = (
        f"{header}"
        f"🌌 <b>{title}</b>\n\n"
        f"{desc_label}\n"
        f"{explanation}"
    )

    keyboard = get_apod_actions_inline(
        nasa_url=apod_url,
        hd_url=hd_url,
        is_random=is_random,
        is_birthday=is_birthday,
        lang=lang,
    )

    if media_type == "image" and apod_url:
        # Лимит подписи к фото в Telegram — 1024 символа
        if len(caption_full) <= 1024:
            try:
                await message.answer_photo(
                    photo=apod_url,
                    caption=caption_full,
                    reply_markup=keyboard,
                )
                return
            except Exception as e:
                logger.warning("Failed to send photo with caption: %s", e)

        # Если текст превышает 1024 символа или возникла ошибка — отправляем фото отдельно, затем описание
        try:
            await message.answer_photo(photo=apod_url)
            await message.answer(caption_full, reply_markup=keyboard)
        except Exception as e:
            logger.warning("Failed to send photo: %s. Sending text only.", e)
            await message.answer(caption_full, reply_markup=keyboard)

    elif media_type == "video":
        video_label = get_text("video_label", lang)
        watch_label = get_text("watch_video", lang)
        video_text = (
            f"{caption_full}\n\n"
            f'{video_label} <a href="{apod_url}">{watch_label}</a>'
        )
        await message.answer(video_text, reply_markup=keyboard)
    else:
        await message.answer(caption_full, reply_markup=keyboard)


async def handle_health_check(request: web.Request) -> web.Response:
    return web.Response(text="NASA APOD Bot is running OK 🚀", content_type="text/plain")


async def start_web_server() -> web.AppRunner | None:
    port = int(os.getenv("PORT", "0"))
    if not port:
        # Локальный запуск без PORT
        return None

    app = web.Application()
    app.router.add_get("/", handle_health_check)
    app.router.add_get("/health", handle_health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("🌐 Web-сервер для healthcheck запущен на порту %s", port)
    return runner


# --------------------------- ТОЧКА ВХОДА --------------------------- #


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не задан в .env!")
        return

    # Запуск web-сервера для Render / хостингов, если передан PORT
    runner = await start_web_server()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Регистрация команд в меню Telegram
    try:
        await set_bot_commands(bot)
        logger.info("✅ Команды меню Telegram успешно зарегистрированы.")
    except Exception as e:
        logger.warning("Не удалось зарегистрировать команды меню: %s", e)

    logger.info("🚀 NASA APOD Bot (с поддержкой языков RU/EN) запущен и готов к работе!")
    try:
        await dp.start_polling(bot)
    finally:
        if runner:
            await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")
