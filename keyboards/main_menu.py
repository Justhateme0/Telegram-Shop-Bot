from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PRODUCTS
from database.db_handler import db

async def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = []

    for key, product in PRODUCTS.items():
        if key != "cvv_cc":
            keyboard.append([InlineKeyboardButton(
                text=product["name"],
                callback_data=f"category_{key}"
            )])

    keyboard.append([InlineKeyboardButton(
        text="💳 CVV+CC",
        callback_data="category_cvv_cc"
    )])

    custom_categories = await db.get_categories_with_products()
    for category in custom_categories:
        if category not in [cat for cat in PRODUCTS.keys()]:
            keyboard.append([InlineKeyboardButton(
                text=f"🛍 {category}",
                callback_data=f"custom_category_{category}"
            )])

    keyboard.append([InlineKeyboardButton(
        text="❓ FAQ",
        callback_data="faq"
    )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
    ])