from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from database.db_handler import db
from keyboards.payment_kb import get_admin_menu_keyboard
from config import ADMIN_ID

router = Router()

class AdminStates(StatesGroup):
    waiting_wallet = State()
    waiting_broadcast = State()
    waiting_product_category = State()
    waiting_product_name = State()
    waiting_product_price_rub = State()
    waiting_product_price_usd = State()
    waiting_product_description = State()

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    stats = await db.get_orders_stats()
    users_count = await db.get_users_count()

    text = f"""
🔧 Админ-панель X-STOODERS

📊 Статистика:
• Пользователей: {users_count}
• Всего заказов: {stats['total']}
• Выполнено: {stats['completed']}
• В ожидании: {stats['waiting']}
• На рассмотрении: {stats['pending']}
"""

    await message.answer(text, reply_markup=get_admin_menu_keyboard())

@router.callback_query(F.data == "admin_orders")
async def show_pending_orders(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    orders = await db.get_pending_orders()

    if not orders:
        await callback.message.edit_text(
            "📋 Нет заказов на подтверждение",
            reply_markup=get_admin_menu_keyboard()
        )
        return

    text = "📋 Заказы на подтверждение:\n\n"

    for order in orders[:10]:
        username = f"@{order['username']}" if order['username'] else "без username"
        text += f"🆔 #{order['id']}\n"
        text += f"👤 {order['first_name']} ({username})\n"
        text += f"📦 {order['product_name']}\n"
        text += f"💰 {order['price_rub']}₽ / ${order['price_usd']}\n\n"

    await callback.message.edit_text(text, reply_markup=get_admin_menu_keyboard())

@router.callback_query(F.data == "admin_stats")
async def show_admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    stats = await db.get_orders_stats()
    users_count = await db.get_users_count()
    wallet = await db.get_usdt_wallet()

    text = f"""
📊 Подробная статистика

👥 Пользователи: {users_count}

📦 Заказы:
• Всего: {stats['total']}
• Выполнено: {stats['completed']}
• В ожидании: {stats['waiting']}
• Отложено: {stats['pending']}

💳 USDT кошелек: {wallet or "Не установлен"}
"""

    await callback.message.edit_text(text, reply_markup=get_admin_menu_keyboard())

@router.callback_query(F.data == "admin_wallet")
async def change_wallet(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    await state.set_state(AdminStates.waiting_wallet)

    current_wallet = await db.get_usdt_wallet()
    text = f"💳 Текущий USDT кошелек: {current_wallet or 'Не установлен'}\n\n"
    text += "Введите новый адрес USDT кошелька:"

    await callback.message.edit_text(text)

@router.message(AdminStates.waiting_wallet)
async def save_wallet(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    wallet = message.text.strip()

    if len(wallet) < 10:
        await message.answer("❌ Некорректный адрес кошелька")
        return

    success = await db.set_usdt_wallet(wallet)

    if success:
        await message.answer(
            f"✅ USDT кошелек обновлен:\n<code>{wallet}</code>",
            parse_mode="HTML",
            reply_markup=get_admin_menu_keyboard()
        )
    else:
        await message.answer("❌ Ошибка сохранения кошелька")

    await state.clear()

@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    await state.set_state(AdminStates.waiting_broadcast)

    users_count = await db.get_users_count()
    text = f"📢 Рассылка сообщения\n\n"
    text += f"👥 Будет отправлено {users_count} пользователям\n\n"
    text += "Введите текст сообщения для рассылки:"

    await callback.message.edit_text(text)

@router.message(AdminStates.waiting_broadcast)
async def send_broadcast(message: Message, state: FSMContext, bot):
    if not is_admin(message.from_user.id):
        return

    users = await db.get_all_users()
    broadcast_text = message.text

    sent_count = 0
    failed_count = 0

    status_message = await message.answer(f"📢 Начинаю рассылку для {len(users)} пользователей...")

    for user_id in users:
        try:
            await bot.send_message(user_id, broadcast_text)
            sent_count += 1
        except Exception:
            failed_count += 1

        if (sent_count + failed_count) % 50 == 0:
            await status_message.edit_text(
                f"📢 Рассылка: отправлено {sent_count}, ошибок {failed_count}"
            )

    final_text = f"""
✅ Рассылка завершена!

📊 Результат:
• Отправлено: {sent_count}
• Ошибок: {failed_count}
• Всего пользователей: {len(users)}
"""

    await status_message.edit_text(final_text, reply_markup=get_admin_menu_keyboard())
    await state.clear()

@router.callback_query(F.data.startswith("admin_confirm_"))
async def confirm_payment(callback: CallbackQuery, bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    order_id = int(callback.data.split("_")[2])

    order = await db.get_order(order_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    success = await db.update_order_status(order_id, "completed")

    if success:
        try:
            await callback.message.edit_caption(
                callback.message.caption + "\n\n✅ ОПЛАТА ПОДТВЕРЖДЕНА"
            )
        except Exception:
            await callback.answer("✅ Оплата подтверждена!")

        try:
            await bot.send_message(
                order["user_id"],
                f"✅ Ваш заказ #{order_id} подтвержден!\n\n"
                f"📦 Товар: {order['product_name']}\n"
                f"💰 Сумма: {order['price_rub']}₽ / ${order['price_usd']}\n\n"
                f"📞 Свяжитесь с администратором для получения товара: @skrdllQ"
            )
        except Exception:
            pass
    else:
        await callback.answer("❌ Ошибка подтверждения", show_alert=True)

@router.callback_query(F.data.startswith("admin_decline_"))
async def decline_payment(callback: CallbackQuery, bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    order_id = int(callback.data.split("_")[2])

    order = await db.get_order(order_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    success = await db.update_order_status(order_id, "declined")

    if success:
        try:
            await callback.message.edit_caption(
                callback.message.caption + "\n\n❌ ОПЛАТА ОТКЛОНЕНА"
            )
        except Exception:
            await callback.answer("❌ Оплата отклонена!")

        try:
            await bot.send_message(
                order["user_id"],
                f"❌ Ваш заказ #{order_id} отклонен\n\n"
                f"📦 Товар: {order['product_name']}\n"
                f"Причина: неверная сумма или некорректный скриншот\n\n"
                f"📞 Свяжитесь с администратором: @skrdllQ"
            )
        except Exception:
            pass
    else:
        await callback.answer("❌ Ошибка отклонения", show_alert=True)

@router.callback_query(F.data == "admin_products")
async def show_products_management(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    from keyboards.payment_kb import get_products_management_keyboard

    text = """
🛍 Управление товарами

Здесь вы можете добавлять новые товары и управлять существующими.
Товары будут отображаться в каталоге бота.
"""

    await callback.message.edit_text(text, reply_markup=get_products_management_keyboard())

@router.callback_query(F.data == "admin_back")
async def back_to_admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    stats = await db.get_orders_stats()
    users_count = await db.get_users_count()

    text = f"""
🔧 Админ-панель X-STOODERS

📊 Статистика:
• Пользователей: {users_count}
• Всего заказов: {stats['total']}
• Выполнено: {stats['completed']}
• В ожидании: {stats['waiting']}
• На рассмотрении: {stats['pending']}
"""

    await callback.message.edit_text(text, reply_markup=get_admin_menu_keyboard())

@router.callback_query(F.data == "admin_add_product")
async def start_add_product(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    await state.set_state(AdminStates.waiting_product_category)

    text = """
➕ Добавление нового товара

Шаг 1/5: Введите категорию товара
Примеры: VPN, Прокси, Модели, Анонимные номера и т.д.
"""

    await callback.message.edit_text(text)

@router.message(AdminStates.waiting_product_category)
async def add_product_category(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    category = message.text.strip()
    await state.update_data(category=category)
    await state.set_state(AdminStates.waiting_product_name)

    text = f"""
➕ Добавление нового товара

Категория: {category}

Шаг 2/5: Введите название товара
Например: NordVPN Premium, Rotation 10GB, STANDART модель и т.д.
"""

    await message.answer(text)

@router.message(AdminStates.waiting_product_name)
async def add_product_name(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    name = message.text.strip()
    data = await state.get_data()

    await state.update_data(name=name)
    await state.set_state(AdminStates.waiting_product_price_rub)

    text = f"""
➕ Добавление нового товара

Категория: {data['category']}
Название: {name}

Шаг 3/5: Введите цену в рублях
Введите только число или 0, если цена в рублях не нужна
"""

    await message.answer(text)

@router.message(AdminStates.waiting_product_price_rub)
async def add_product_price_rub(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    try:
        price_rub = int(message.text.strip())
        if price_rub < 0:
            await message.answer("❌ Цена не может быть отрицательной. Введите корректную цену:")
            return
    except ValueError:
        await message.answer("❌ Введите корректное число:")
        return

    data = await state.get_data()
    await state.update_data(price_rub=price_rub if price_rub > 0 else None)
    await state.set_state(AdminStates.waiting_product_price_usd)

    text = f"""
➕ Добавление нового товара

Категория: {data['category']}
Название: {data['name']}
Цена в рублях: {price_rub if price_rub > 0 else 'не указана'}

Шаг 4/5: Введите цену в долларах
Введите только число или 0, если цена в долларах не нужна
"""

    await message.answer(text)

@router.message(AdminStates.waiting_product_price_usd)
async def add_product_price_usd(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    try:
        price_usd = int(message.text.strip())
        if price_usd < 0:
            await message.answer("❌ Цена не может быть отрицательной. Введите корректную цену:")
            return
    except ValueError:
        await message.answer("❌ Введите корректное число:")
        return

    data = await state.get_data()
    await state.update_data(price_usd=price_usd if price_usd > 0 else None)
    await state.set_state(AdminStates.waiting_product_description)

    text = f"""
➕ Добавление нового товара

Категория: {data['category']}
Название: {data['name']}
Цена в рублях: {data.get('price_rub') or 'не указана'}
Цена в долларах: {price_usd if price_usd > 0 else 'не указана'}

Шаг 5/5: Введите описание товара (необязательно)
Введите описание или отправьте "пропустить"
"""

    await message.answer(text)

@router.message(AdminStates.waiting_product_description)
async def add_product_description(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    description = message.text.strip()
    if description.lower() == "пропустить":
        description = None

    data = await state.get_data()

    success = await db.add_custom_product(
        category=data['category'],
        name=data['name'],
        price_rub=data.get('price_rub'),
        price_usd=data.get('price_usd'),
        description=description
    )

    if success:
        price_text = ""
        if data.get('price_rub'):
            price_text += f"{data['price_rub']}₽"
        if data.get('price_usd'):
            if price_text:
                price_text += f" / ${data['price_usd']}"
            else:
                price_text = f"${data['price_usd']}"
        if not price_text:
            price_text = "По запросу"

        text = f"""
✅ Товар успешно добавлен!

📦 {data['name']}
📂 Категория: {data['category']}
💰 Цена: {price_text}
📝 Описание: {description or 'не указано'}

Товар будет доступен в каталоге бота.
"""

        from keyboards.payment_kb import get_products_management_keyboard

        await message.answer(text, reply_markup=get_products_management_keyboard())
    else:
        await message.answer("❌ Ошибка добавления товара. Попробуйте еще раз.")

    await state.clear()

@router.callback_query(F.data == "admin_list_products")
async def list_products(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    products = await db.get_custom_products()

    if not products:
        from keyboards.payment_kb import get_products_management_keyboard

        await callback.message.edit_text(
            "📝 Список товаров пуст\n\nДобавьте товары через кнопку 'Добавить товар'",
            reply_markup=get_products_management_keyboard()
        )
        return

    keyboard = []

    for product in products:
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
            callback_data=f"admin_view_product_{product['id']}"
        )])

    keyboard.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="admin_products"
    )])

    from aiogram.types import InlineKeyboardMarkup

    await callback.message.edit_text(
        f"📝 Список товаров ({len(products)} шт.)\n\nВыберите товар для управления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

@router.callback_query(F.data.startswith("admin_view_product_"))
async def view_product(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    product_id = int(callback.data.split("_")[3])
    product = await db.get_product_by_id(product_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    price_text = ""
    if product['price_rub'] and product['price_usd']:
        price_text = f"{product['price_rub']}₽ / ${product['price_usd']}"
    elif product['price_rub']:
        price_text = f"{product['price_rub']}₽"
    elif product['price_usd']:
        price_text = f"${product['price_usd']}"
    else:
        price_text = "По запросу"

    text = f"""
📦 {product['name']}

📂 Категория: {product['category']}
💰 Цена: {price_text}
📝 Описание: {product['description'] or 'не указано'}
🔧 Статус: {'Активен' if product['availability'] else 'Отключен'}
🆔 ID: {product['id']}
"""

    from keyboards.payment_kb import get_product_actions_keyboard

    await callback.message.edit_text(text, reply_markup=get_product_actions_keyboard(product_id))

@router.callback_query(F.data.startswith("admin_delete_product_"))
async def confirm_delete_product(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    product_id = int(callback.data.split("_")[3])
    product = await db.get_product_by_id(product_id)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text = f"""
🗑 Удаление товара

📦 {product['name']}
📂 Категория: {product['category']}

⚠️ Внимание! Это действие нельзя отменить.
Все заказы этого товара останутся в истории.

Вы уверены, что хотите удалить товар?
"""

    from keyboards.payment_kb import get_confirm_delete_keyboard

    await callback.message.edit_text(text, reply_markup=get_confirm_delete_keyboard(product_id))

@router.callback_query(F.data.startswith("admin_confirm_delete_"))
async def delete_product(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    product_id = int(callback.data.split("_")[3])

    success = await db.delete_custom_product(product_id)

    if success:
        await callback.answer("✅ Товар удален")

        products = await db.get_custom_products()

        if not products:
            from keyboards.payment_kb import get_products_management_keyboard

            await callback.message.edit_text(
                "📝 Список товаров пуст\n\nДобавьте товары через кнопку 'Добавить товар'",
                reply_markup=get_products_management_keyboard()
            )
        else:
            await list_products(callback)
    else:
        await callback.answer("❌ Ошибка удаления товара", show_alert=True)

@router.callback_query(F.data.startswith("admin_disable_product_"))
async def disable_product(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступ запрещен", show_alert=True)
        return

    product_id = int(callback.data.split("_")[3])

    success = await db.update_product_availability(product_id, False)

    if success:
        await callback.answer("✅ Товар отключен")
        await view_product(callback)
    else:
        await callback.answer("❌ Ошибка отключения товара", show_alert=True)