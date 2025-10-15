import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
USDT_WALLET = os.getenv("USDT_WALLET")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot_database.db")

PRODUCTS: Dict[str, Dict[str, Any]] = {
    "models": {
        "name": "📱 Модели для работы",
        "items": {
            "STANDART": {"rub": 999, "usd": 10},
            "DIAMOND": {"rub": 2499, "usd": 25},
            "PREMIUM": {"rub": 3699, "usd": 37},
            "Профурсетка": {"rub": 6499, "usd": 65},
            "EXCLUSIVE": {"rub": 9849, "usd": 98}
        }
    },
    "packs": {
        "name": "📦 Паки",
        "items": {
            "Продуктивный воркер": {"rub": 1500, "usd": 15},
            "Продвинутый воркер": {"rub": 3429, "usd": 34},
            "Расходники": {"rub": 2999, "usd": 30},
            "Уверенный воркер": {"rub": 1799, "usd": 18}
        }
    },
    "anonymous_numbers": {
        "name": "📞 Анонимные номера",
        "items": {
            "1 месяц": {"rub": 12599, "usd": 126},
            "2 месяца": {"rub": 19999, "usd": 200},
            "3 месяца": {"rub": 30999, "usd": 310}
        }
    },
    "physical_numbers": {
        "name": "🔢 Физические номера",
        "items": {
            "Польша": {"rub": 2999, "usd": 30},
            "Чехия": {"rub": 7599, "usd": 76},
            "Франция": {"rub": 8999, "usd": 90}
        }
    },
    "proxy": {
        "name": "🌐 Прокси",
        "items": {
            "Rotation 1 GB": {"rub": 1199, "usd": 12},
            "Rotation 5 GB": {"rub": 4999, "usd": 50},
            "Rotation 15 GB": {"rub": 10499, "usd": 105},
            "Regular 1 месяц": {"rub": 759, "usd": 8},
            "Regular 3 месяца": {"rub": 1599, "usd": 16},
            "Regular 6 месяцев": {"rub": 2399, "usd": 24},
            "Regular 9 месяцев": {"rub": 3299, "usd": 33},
            "Regular 12 месяцев": {"rub": 4599, "usd": 46}
        }
    },
    "vpn": {
        "name": "🔒 VPN",
        "items": {
            "PURE VPN": {"rub": 529, "usd": 5},
            "Windscribe Pro": {"rub": 459, "usd": 5},
            "TunnelBear": {"rub": 379, "usd": 4},
            "NordVPN": {"rub": 379, "usd": 4},
            "PIA VPN": {"rub": 499, "usd": 5},
            "VPN + Гайд": {"rub": 1500, "usd": 15}
        }
    },
    "telegram_premium": {
        "name": "💎 Telegram Premium",
        "items": {
            "1 месяц": {"rub": 1099, "usd": 11},
            "3 месяца": {"rub": 3199, "usd": 32},
            "6 месяцев": {"rub": 3899, "usd": 39},
            "12 месяцев": {"rub": 5499, "usd": 55}
        }
    },
    "discord": {
        "name": "💎 Discord",
        "items": {
            "Nitro 1 месяц": {"rub": 1229, "usd": 12},
            "Nitro 6 месяцев": {"rub": 6199, "usd": 62},
            "Nitro 24 месяца": {"rub": 18299, "usd": 183},
            "Boost 4 шт": {"rub": 500, "usd": 5},
            "Boost 6 шт": {"rub": 750, "usd": 8},
            "Boost 8 шт": {"rub": 950, "usd": 10},
            "Boost 10 шт": {"rub": 1200, "usd": 12},
            "Boost 12 шт": {"rub": 1450, "usd": 15},
            "Boost 14 шт": {"rub": 1700, "usd": 17}
        }
    },
    "telegram_channels": {
        "name": "📢 Каналы Telegram",
        "items": {
            "STANDART": {"rub": 23999, "usd": 240},
            "DIAMOND": {"rub": 35999, "usd": 360},
            "PREMIUM": {"rub": 59999, "usd": 600}
        }
    },
    "design": {
        "name": "🎨 Разработка дизайна",
        "items": {
            "DEFAULT": {"rub": 1499, "usd": 15},
            "DIAMOND": {"rub": 2199, "usd": 22},
            "PREMIUM": {"rub": 2999, "usd": 30},
            "GOLD": {"rub": 18599, "usd": 186},
            "PREMIUM крупный пакет": {"rub": 31199, "usd": 312}
        }
    },
    "cvv_cc": {
        "name": "💳 CVV+CC",
        "items": {
            "ING": {"usd": 60},
            "BNP Paribas": {"usd": 63},
            "UniCredit": {"usd": 77},
            "UnionPay": {"usd": 68},
            "PNC": {"usd": 42},
            "TD Bank": {"usd": 56},
            "Bank of America": {"usd": 90},
            "Kaspi": {"usd": 20},
            "CBA": {"usd": 40},
            "Westpac": {"usd": 46},
            "NAB": {"usd": 55},
            "ANZ": {"usd": 50}
        }
    }
}

FAQ_TEXT = """
🛍 X-STOODERS • FAQ

👥 Официальные контакты:
┠ Администратор: @skrdllQ

💡 Обращайтесь по всем вопросам строго в рабочие часы!

✅ Товар выдаётся лично в ЛС после получения скриншота о переводе.

💰 Способ оплаты: USDT TRC20 (TRON)
"""