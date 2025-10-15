from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import uuid
from database.db_handler import db
from keyboards.payment_kb import get_payment_keyboard
from keyboards.main_menu import get_main_menu
from config import PRODUCTS, USDT_WALLET, ADMIN_ID

router = Router()

class PaymentStates(StatesGroup):
    waiting_screenshot = State()

user_orders = {}

@router.callback_query(F.data.startswith("buy_"))
async def start_purchase(callback: CallbackQuery, state: FSMContext):
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

    price_rub = product_data.get("rub")
    price_usd = product_data.get("usd")

    order_id = await db.create_order(
        user_id=callback.from_user.id,
        product_category=category,
        product_name=product_name,
        price_rub=price_rub,
        price_usd=price_usd
    )

    if not order_id:
        await callback.answer("Ошибка создания заказа", show_alert=True)
        return

    user_orders[callback.from_user.id] = order_id

    order_uuid = str(uuid.uuid4())[:8].upper()

    text = f"""
🛒 Заказ #{order_uuid}

📦 Товар: {product_name}
📂 Категория: {PRODUCTS[category]['name']}

💰 К оплате:
"""

    if price_rub and price_usd:
        text += f"• {price_rub} ₽ или ${price_usd} USD\n"
    elif price_usd:
        text += f"• ${price_usd} USD\n"
    elif price_rub:
        text += f"• {price_rub} ₽\n"

    wallet = await db.get_usdt_wallet() or USDT_WALLET

    text += f"""
💳 Адрес для оплаты USDT (TRC20):
<code>{wallet}</code>

📋 Инструкция:
1. Переведите точную сумму на указанный адрес
2. Сделайте скриншот транзакции
3. Отправьте скриншот, нажав кнопку ниже

⚠️ Внимание: переводите точную сумму в USDT TRC20!
"""

    await callback.message.edit_text(
        text,
        reply_markup=get_payment_keyboard(order_id),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("upload_screenshot_"))
async def request_screenshot(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split("_")[2])

    order = await db.get_order(order_id)
    if not order or order["user_id"] != callback.from_user.id:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    await state.set_state(PaymentStates.waiting_screenshot)
    await state.update_data(order_id=order_id)

    await callback.message.edit_text(
        "📸 Отправьте скриншот оплаты одним сообщением:"
    )

@router.message(PaymentStates.waiting_screenshot, F.photo)
async def handle_screenshot(message: Message, state: FSMContext, bot):
    data = await state.get_data()
    order_id = data.get("order_id")

    if not order_id:
        await message.answer("Ошибка: заказ не найден")
        await state.clear()
        return

    order = await db.get_order(order_id)
    if not order:
        await message.answer("Заказ не найден")
        await state.clear()
        return

    file_id = message.photo[-1].file_id
    success = await db.add_payment_screenshot(order_id, file_id)

    if success:
        await message.answer(
            "✅ Скриншот получен!\n\n"
            "Ваш заказ отправлен на проверку администратору.\n"
            "Ожидайте подтверждения оплаты.",
            reply_markup=await get_main_menu()
        )

        if ADMIN_ID:
            try:
                user = await db.get_user(message.from_user.id)
                username = f"@{user['username']}" if user['username'] else "без username"

                admin_text = f"""
🔔 Новый заказ на подтверждение!

👤 Покупатель: {user['first_name']} ({username})
📦 Товар: {order['product_name']}
📂 Категория: {order['product_category']}
💰 Сумма: {order['price_rub']}₽ / ${order['price_usd']}
🆔 ID заказа: {order_id}
"""

                from keyboards.payment_kb import get_admin_order_keyboard

                await bot.send_photo(
                    ADMIN_ID,
                    file_id,
                    caption=admin_text,
                    reply_markup=get_admin_order_keyboard(order_id)
                )
            except Exception:
                pass
    else:
        await message.answer("❌ Ошибка сохранения скриншота. Попробуйте еще раз.")

    await state.clear()

@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[2])

    order = await db.get_order(order_id)
    if not order or order["user_id"] != callback.from_user.id:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    success = await db.update_order_status(order_id, "cancelled")

    if success:
        await callback.message.edit_text(
            "❌ Заказ отменен",
            reply_markup=await get_main_menu()
        )
    else:
        await callback.answer("Ошибка отмены заказа", show_alert=True)

@router.callback_query(F.data.startswith("buy_custom_"))
async def start_custom_purchase(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[2])

    product = await db.get_product_by_id(product_id)
    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    order_id = await db.create_order(
        user_id=callback.from_user.id,
        product_category=product['category'],
        product_name=product['name'],
        price_rub=product['price_rub'],
        price_usd=product['price_usd']
    )

    if not order_id:
        await callback.answer("Ошибка создания заказа", show_alert=True)
        return

    user_orders[callback.from_user.id] = order_id

    order_uuid = str(uuid.uuid4())[:8].upper()

    text = f"""
🛒 Заказ #{order_uuid}

📦 Товар: {product['name']}
📂 Категория: {product['category']}

💰 К оплате:
"""

    if product['price_rub'] and product['price_usd']:
        text += f"• {product['price_rub']} ₽ или ${product['price_usd']} USD\n"
    elif product['price_usd']:
        text += f"• ${product['price_usd']} USD\n"
    elif product['price_rub']:
        text += f"• {product['price_rub']} ₽\n"
    else:
        text += "• По запросу - свяжитесь с администратором\n"

    wallet = await db.get_usdt_wallet() or USDT_WALLET

    text += f"""
💳 Адрес для оплаты USDT (TRC20):
<code>{wallet}</code>

📋 Инструкция:
1. Переведите точную сумму на указанный адрес
2. Сделайте скриншот транзакции
3. Отправьте скриншот, нажав кнопку ниже

⚠️ Внимание: переводите точную сумму в USDT TRC20!
"""

    await callback.message.edit_text(
        text,
        reply_markup=get_payment_keyboard(order_id),
        parse_mode="HTML"
    )