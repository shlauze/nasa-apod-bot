import json
import logging
import os

SETTINGS_FILE = "user_settings.json"
logger = logging.getLogger(__name__)

_memory_cache: dict[int, dict] = {}


def _load_settings() -> dict:
    global _memory_cache
    if _memory_cache:
        return _memory_cache

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert string keys to int user_ids
                _memory_cache = {int(k): v for k, v in data.items()}
                return _memory_cache
        except Exception as e:
            logger.error("Failed to read %s: %s", SETTINGS_FILE, e)
            _memory_cache = {}
    return _memory_cache


def _save_settings():
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_memory_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("Failed to save %s: %s", SETTINGS_FILE, e)


def get_user_language(user_id: int, telegram_lang: str | None = None) -> str:
    """Возвращает язык пользователя ('ru' или 'en')."""
    settings = _load_settings()
    if user_id in settings and "lang" in settings[user_id]:
        return settings[user_id]["lang"]

    # Автоопределение по telegram_lang
    if telegram_lang and telegram_lang.startswith("en"):
        default_lang = "en"
    else:
        default_lang = "ru"

    set_user_language(user_id, default_lang)
    return default_lang


def set_user_language(user_id: int, lang: str):
    """Сохраняет выбранный язык пользователя."""
    settings = _load_settings()
    if user_id not in settings:
        settings[user_id] = {}
    settings[user_id]["lang"] = lang
    _save_settings()
