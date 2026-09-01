import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY").strip()

if not BOT_TOKEN:
    # Сообщение с подсказкой при отсутствии токена
    pass
