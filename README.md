# 🌌 NASA APOD Telegram Bot

Telegram-бот для просмотра **Astronomy Picture of the Day (APOD)** от NASA.

Поддерживает двуязычный интерфейс (RU/EN), выбор случайных снимков, просмотр снимка за конкретную дату и на день рождения.

---

## ✨ Возможности

- 🌌 **APOD за сегодня**: просмотр актуального космического снимка дня с описанием.
- 🎲 **Случайный снимок**: просмотр случайного APOD за всю историю архива (с 16 июня 1995 года).
- 📅 **Выбор даты**: ввод любой интересующей даты в удобном формате (`ДД.ММ.ГГГГ`, `ГГГГ-ММ-ДД` и др.).
- 🎂 **APOD в день рождения**: просмотр снимка, опубликованного в день вашего рождения (с поддержкой выбора года для родившихся до июня 1995 года).
- 🌐 **Двуязычность**: поддержка русского и английского языков с возможностью переключения в любой момент.
- 🔍 **HD качество**: кнопка перехода к оригинальному изображению в высоком разрешении.
- 🔗 **Ссылки на NASA**: прямой переход на официальную страницу APOD.

---

## 🛠 Технологии

- **Python 3.10+**
- **[aiogram 3.x](https://github.com/aiogram/aiogram)** — асинхронный фреймворк для Telegram Bot API
- **[aiohttp](https://github.com/aio-libs/aiohttp)** — асинхронные HTTP-запросы к NASA API
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — управление переменными окружения

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/YOUR_USERNAME/nasa-apod-bot.git
cd nasa-apod-bot
```

### 2. Создание и активация виртуального окружения
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` в корне проекта (на основе `.env.example`):
```env
BOT_TOKEN=ваш_токен_бота_от_BotFather
NASA_API_KEY=ваш_ключ_nasa_или_DEMO_KEY
```
- Получить токен бота: [@BotFather](https://t.me/BotFather) в Telegram.
- Получить NASA API Key: [api.nasa.gov](https://api.nasa.gov/) *(можно использовать `DEMO_KEY` для тестов)*.

### 5. Запуск бота
```bash
python bot.py
```

---

## 📁 Структура проекта

```text
├── bot.py                # Главный файл запуска и обработчики событий
├── config.py             # Загрузка конфигурации из .env
├── keyboards.py          # Инлайн-клавиатуры и меню
├── locales.py            # Тексты и локализация (RU / EN)
├── nasa.py               # Взаимодействие с NASA APOD API
├── states.py             # FSM состояния (ввод даты/дня рождения)
├── storage.py            # Хранение настроек пользователей
├── requirements.txt      # Список зависимостей
├── .env.example          # Пример файла конфигурации
└── .gitignore            # Игнорируемые файлы Git
```
