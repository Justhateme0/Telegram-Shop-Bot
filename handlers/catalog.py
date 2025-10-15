from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import PRODUCTS
from keyboards.catalog_kb import get_category_keyboard, get_product_keyboard

router = Router()

@router.callback_query(F.data.startswith("category_"))
async def show_category(callback: CallbackQuery):
    category = callback.data.split("_", 1)[1]

    if category not in PRODUCTS:
        await callback.answer("Категория не найдена", show_alert=True)
        return

    category_name = PRODUCTS[category]["name"]
    text = f"{category_name}\n\nВыберите товар:"

    await callback.message.edit_text(
        text,
        reply_markup=get_category_keyboard(category)
    )

@router.callback_query(F.data.startswith("product_"))
async def show_product(callback: CallbackQuery):
    parts = callback.data.split("_", 2)
    if len(parts) < 3:
        await callback.answer("Неверный формат данных", show_alert=True)
        return

    category = parts[1]
    product_name = parts[2]

    if category not in PRODUCTS or product_name not in PRODUCTS[category]["items"]:
        await callback.answer("Товар не найден", show_alert=True)
        return

    product_data = PRODUCTS[category]["items"][product_name]
    category_name = PRODUCTS[category]["name"]

    text = f"📦 {product_name}\n"
    text += f"📂 Категория: {category_name}\n\n"

    text += "💰 Цена:\n"
    if "rub" in product_data and "usd" in product_data:
        text += f"• {product_data['rub']} ₽\n"
        text += f"• ${product_data['usd']} USD\n"
    elif "usd" in product_data:
        text += f"• ${product_data['usd']} USD\n"
    elif "rub" in product_data:
        text += f"• {product_data['rub']} ₽\n"
    else:
        text += "• По запросу\n"

    text += "\n💰 Способ оплаты: USDT TRC20 (TRON)\n"
    text += "✅ Товар выдаётся лично в ЛС после подтверждения оплаты"

    await callback.message.edit_text(
        text,
        reply_markup=get_product_keyboard(category, product_name)
    )

@router.callback_query(F.data.startswith("custom_category_"))
async def show_custom_category(callback: CallbackQuery):
    category = callback.data.split("_", 2)[2]

    products = await db.get_custom_products()
    category_products = [p for p in products if p['category'] == category]

    if not category_products:
        await callback.answer("В этой категории нет товаров", show_alert=True)
        return

    keyboard = []

    for product in category_products:
        price_text = ""
        if product['price_rub'] and product['price_usd']:
            price_text = f" - {product['price_rub']}₽/${product['price_usd']}"
        elif product['price_rub']:
            price_text = f" - {product['price_rub']}₽"
        elif product['price_usd']:
            price_text = f" - ${product['price_usd']}"

        button_text = f"{product['name']}{price_text}"

        keyboard.append([InlineKeyboardButton(
            text=button_text,
            callback_data=f"custom_product_{product['id']}"
        )])

    keyboard.append([InlineKeyboardButton(
        text="🔙 Назад в меню",
        callback_data="main_menu"
    )])

    from aiogram.types import InlineKeyboardMarkup

    await callback.message.edit_text(
        f"🛍 {category}\n\nВыберите товар:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

@router.callback_query(F.data.startswith("custom_product_"))
async def show_custom_product(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[2])

    from database.db_handler import db
    product = await db.get_product_by_id(product_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text = f"📦 {product['name']}\n"
    text += f"📂 Категория: {product['category']}\n\n"

    text += "💰 Цена:\n"
    if product['price_rub'] and product['price_usd']:
        text += f"• {product['price_rub']} ₽\n"
        text += f"• ${product['price_usd']} USD\n"
    elif product['price_usd']:
        text += f"• ${product['price_usd']} USD\n"
    elif product['price_rub']:
        text += f"• {product['price_rub']} ₽\n"
    else:
        text += "• По запросу\n"

    if product['description']:
        text += f"\n📝 Описание:\n{product['description']}\n"

    text += "\n💰 Способ оплаты: USDT TRC20 (TRON)\n"
    text += "✅ Товар выдаётся лично в ЛС после подтверждения оплаты"

    keyboard = [
        [InlineKeyboardButton(
            text="💰 Купить",
            callback_data=f"buy_custom_{product['id']}"
        )],
        [InlineKeyboardButton(
            text="🔙 Назад к категории",
            callback_data=f"custom_category_{product['category']}"
        )],
        [InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="main_menu"
        )]
    ]

    from aiogram.types import InlineKeyboardMarkup

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )