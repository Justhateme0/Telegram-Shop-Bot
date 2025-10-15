import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db_handler import init_database
from handlers import start, catalog, payment, admin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def main():
    if not BOT_TOKEN:
        logger.error("Bot token not found! Please set BOT_TOKEN in .env file")
        return

    Path("logs").mkdir(exist_ok=True)

    logger.info("Starting X-STOODERS Bot...")

    try:
        await init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return

    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)

    logger.info("Bot started successfully!")

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        if "Bad Gateway" in str(e) or "Service Unavailable" in str(e):
            logger.info("Temporary server error, restarting...")
            await asyncio.sleep(5)
            await bot.session.close()
            await main()
    finally:
        await bot.session.close()
        logger.info("Bot session closed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown completed")