import logging
from typing import Optional
from aiogram import Bot
from config import ADMIN_ID

logger = logging.getLogger(__name__)

async def notify_admin(bot: Bot, message: str, order_id: Optional[int] = None) -> bool:
    if not ADMIN_ID:
        logger.warning("Admin ID not set, cannot send notification")
        return False

    try:
        notification_text = f"🔔 Уведомление администратору\n\n{message}"

        if order_id:
            notification_text += f"\n\n🆔 ID заказа: {order_id}"

        await bot.send_message(ADMIN_ID, notification_text)
        logger.info(f"Admin notification sent: {message}")
        return True
    except Exception as e:
        logger.error(f"Failed to send admin notification: {e}")
        return False

async def notify_user(bot: Bot, user_id: int, message: str) -> bool:
    try:
        await bot.send_message(user_id, message)
        logger.info(f"User notification sent to {user_id}: {message}")
        return True
    except Exception as e:
        logger.error(f"Failed to send user notification to {user_id}: {e}")
        return False