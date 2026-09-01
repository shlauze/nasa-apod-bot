from datetime import date

# pyrefly: ignore [missing-import]
import aiohttp

from config import NASA_API_KEY

NASA_URL = "https://api.nasa.gov/planetary/apod"
MIN_DATE = date(1995, 6, 16)


async def get_apod(apod_date: date) -> dict:
    params = {
        "api_key": NASA_API_KEY,
        "date": apod_date.isoformat(),
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(NASA_URL, params=params) as response:
            if response.status == 404:
                raise ValueError("APOD для этой даты не найден.")
            if response.status == 429:
                raise RuntimeError("Превышен лимит запросов к NASA API. Попробуйте позже или используйте персональный ключ.")
            if response.status != 200:
                error_body = await response.text()
                raise RuntimeError(
                    f"NASA API вернул ошибку {response.status}: {error_body}"
                )
            return await response.json()
