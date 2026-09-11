import html
import logging
import re
import urllib.parse
# pyrefly: ignore [missing-import]
import aiohttp

logger = logging.getLogger(__name__)

# Память для кэширования: {(text, target_lang): translated_text}
_translation_cache: dict[tuple[str, str], str] = {}

# Заголовки для имитации браузера
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


async def _translate_google_mobile(text: str, target_lang: str) -> str | None:
    """Переводит текст через мобильный интерфейс Google Translate."""
    url = "https://translate.google.com/m"
    params = {
        "sl": "auto",
        "tl": target_lang,
        "q": text,
    }
    timeout = aiohttp.ClientTimeout(total=8)
    async with aiohttp.ClientSession(headers=_HEADERS, timeout=timeout) as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return None
            body = await resp.text()

            # Быстрый поиск переведенного текста в контейнере div
            match = re.search(r'<div class="(?:result-container|t0)">([\s\S]*?)</div>', body)
            if match:
                raw_translated = match.group(1).strip()
                return html.unescape(raw_translated)
    return None


async def translate_text(text: str, target_lang: str = "ru") -> str:
    """
    Переводит текст на указанный язык (по умолчанию русский).
    Если целевой язык 'en' или текст пустой — возвращает исходный текст.
    Результаты сохраняются в кэш. При ошибке возвращает исходный текст.
    """
    if not text or not text.strip() or target_lang == "en":
        return text

    cache_key = (text.strip(), target_lang)
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    try:
        translated = await _translate_google_mobile(text, target_lang)
        if translated:
            _translation_cache[cache_key] = translated
            return translated
    except Exception as e:
        logger.warning("Ошибка при переводе на '%s': %s", target_lang, e)

    # В случае сбоя возвращаем оригинальный текст
    return text
