from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PRODUCTS

def get_category_keyboard(category: str) -> InlineKeyboardMarkup:
    if category not in PRODUCTS:
        return get_back_keyboard()

    keyboard = []
    items = PRODUCTS[category]["items"]

    for item_name, prices in items.items():
        if "usd" in prices and "rub" in prices:
            price_text = f"{prices['rub']}₽ / ${prices['usd']}"
        elif "usd" in prices:
            price_text = f"${prices['usd']}"
        elif "rub" in prices:
            price_text = f"{prices['rub']}₽"
        else:
            price_text = "По запросу"

        keyboard.append([InlineKeyboardButton(
            text=f"{item_name} - {price_text}",
            callback_data=f"product_{category}_{item_name}"
        )])

    keyboard.append([InlineKeyboardButton(
        text="🔙 Назад в меню",
        callback_data="main_menu"
    )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_product_keyboard(category: str, product_name: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="💰 Купить",
            callback_data=f"buy_{category}_{product_name}"
        )],
        [InlineKeyboardButton(
            text="🔙 Назад к категории",
            callback_data=f"category_{category}"
        )],
        [InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="main_menu"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
    ])