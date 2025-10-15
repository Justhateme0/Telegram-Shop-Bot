from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_payment_keyboard(order_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="📸 Отправить скриншот оплаты",
            callback_data=f"upload_screenshot_{order_id}"
        )],
        [InlineKeyboardButton(
            text="❌ Отменить заказ",
            callback_data=f"cancel_order_{order_id}"
        )],
        [InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="main_menu"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="✅ Подтвердить оплату",
            callback_data=f"admin_confirm_{order_id}"
        )],
        [InlineKeyboardButton(
            text="❌ Отклонить оплату",
            callback_data=f"admin_decline_{order_id}"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="📋 Заказы на подтверждение",
            callback_data="admin_orders"
        )],
        [InlineKeyboardButton(
            text="📊 Статистика",
            callback_data="admin_stats"
        )],
        [InlineKeyboardButton(
            text="🛍 Управление товарами",
            callback_data="admin_products"
        )],
        [InlineKeyboardButton(
            text="💳 Изменить USDT кошелек",
            callback_data="admin_wallet"
        )],
        [InlineKeyboardButton(
            text="📢 Рассылка",
            callback_data="admin_broadcast"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_products_management_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="➕ Добавить товар",
            callback_data="admin_add_product"
        )],
        [InlineKeyboardButton(
            text="📝 Список товаров",
            callback_data="admin_list_products"
        )],
        [InlineKeyboardButton(
            text="🔙 Назад в админ-панель",
            callback_data="admin_back"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_product_actions_keyboard(product_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="🗑 Удалить товар",
            callback_data=f"admin_delete_product_{product_id}"
        )],
        [InlineKeyboardButton(
            text="❌ Отключить товар",
            callback_data=f"admin_disable_product_{product_id}"
        )],
        [InlineKeyboardButton(
            text="🔙 Назад к списку",
            callback_data="admin_list_products"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_confirm_delete_keyboard(product_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="✅ Да, удалить",
            callback_data=f"admin_confirm_delete_{product_id}"
        )],
        [InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="admin_list_products"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)