# 🛍️ X-STOODERS Bot | Telegram Shop Bot

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## 🇬🇧 English

### Hey there! 👋

This is my Telegram bot for X-STOODERS shop. Built it to make online shopping smooth and easy right inside Telegram.

### 🚀 What it does

- **Product Catalog** - Browse through items with ease
- **Payment System** - Secure payment processing
- **Admin Panel** - Manage products and orders on the fly
- **User Notifications** - Keep customers in the loop
- **Database** - SQLite for storing all the important stuff

### 🛠️ Tech Stack

- **Python 3.10+** - The backbone
- **aiogram 3.10.0** - Telegram Bot API wrapper
- **SQLite** - Lightweight database
- **aiosqlite** - Async database operations
- **Pillow** - Image processing

### 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Justhateme0/x_stooders_bot.git
cd x_stooders_bot

# Install dependencies
pip install -r requirements.txt

# Set up your environment
# Create .env file and add:
# BOT_TOKEN=your_bot_token_here

# Run the bot
python bot.py
```

### 📂 Project Structure

```
x_stooders_bot/
├── bot.py              # Main bot file
├── config.py           # Configuration
├── database/           # Database handlers and models
├── handlers/           # Command and callback handlers
│   ├── start.py       # Start command
│   ├── catalog.py     # Product catalog
│   ├── payment.py     # Payment processing
│   └── admin.py       # Admin panel
├── keyboards/          # Bot keyboards
└── utils/             # Helper functions
```

### 💡 Features in Detail

- **Smart Catalog Navigation** - Easy browsing with inline keyboards
- **Payment Integration** - Process orders securely
- **Admin Tools** - Add, edit, and remove products
- **Logging System** - Track everything that happens
- **Error Handling** - Auto-restart on connection issues

### 📝 TODO

- [ ] Add more payment methods
- [ ] Implement order tracking
- [ ] Add product reviews
- [ ] Multi-language support

### 🤝 Connect with Me

- **GitHub**: [@Justhateme0](https://github.com/Justhateme0)
- **Telegram**: [@bossinternet](https://t.me/bossinternet)

### 📄 License

Feel free to use this project however you want. Just give credit where it's due!

---

<a name="russian"></a>
## 🇷🇺 Русский

### Привет! 👋

Это мой Telegram бот для магазина X-STOODERS. Сделал его, чтобы люди могли удобно делать покупки прямо в телеге.

### 🚀 Что умеет

- **Каталог товаров** - Удобный просмотр всех позиций
- **Система оплаты** - Безопасная обработка платежей
- **Админ-панель** - Управление товарами и заказами
- **Уведомления** - Держим клиентов в курсе
- **База данных** - SQLite для хранения всего важного

### 🛠️ Технологии

- **Python 3.10+** - Основа всего
- **aiogram 3.10.0** - Библиотека для Telegram Bot API
- **SQLite** - Легковесная база данных
- **aiosqlite** - Асинхронная работа с БД
- **Pillow** - Обработка изображений

### 📦 Установка

```bash
# Клонируем репозиторий
git clone https://github.com/Justhateme0/x_stooders_bot.git
cd x_stooders_bot

# Ставим зависимости
pip install -r requirements.txt

# Настраиваем окружение
# Создай файл .env и добавь:
# BOT_TOKEN=твой_токен_бота

# Запускаем бота
python bot.py
```

### 📂 Структура проекта

```
x_stooders_bot/
├── bot.py              # Главный файл бота
├── config.py           # Конфигурация
├── database/           # Обработчики БД и модели
├── handlers/           # Обработчики команд и колбэков
│   ├── start.py       # Команда старт
│   ├── catalog.py     # Каталог товаров
│   ├── payment.py     # Обработка платежей
│   └── admin.py       # Админ-панель
├── keyboards/          # Клавиатуры бота
└── utils/             # Вспомогательные функции
```

### 💡 Фичи подробнее

- **Умная навигация по каталогу** - Легкий просмотр через inline-клавиатуры
- **Интеграция платежей** - Безопасная обработка заказов
- **Инструменты админа** - Добавление, редактирование и удаление товаров
- **Система логирования** - Отслеживаем все происходящее
- **Обработка ошибок** - Автоперезапуск при проблемах с соединением

### 📝 Планы на будущее

- [ ] Добавить больше способов оплаты
- [ ] Реализовать отслеживание заказов
- [ ] Добавить отзывы о товарах
- [ ] Поддержка нескольких языков

### 🤝 Связь со мной

- **GitHub**: [@Justhateme0](https://github.com/Justhateme0)
- **Telegram**: [@bossinternet](https://t.me/bossinternet)

### 📄 Лицензия

Можешь использовать этот проект как хочешь. Просто не забудь указать автора!

---

<div align="center">

Made with ❤️ by [@Justhateme0](https://github.com/Justhateme0)

**Star ⭐ this repo if you find it useful!**

</div>
