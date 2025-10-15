from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database.db_handler import db
from keyboards.main_menu import get_main_menu
from config import FAQ_TEXT

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await db.add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )

    welcome_text = f"""
🛍 Добро пожаловать в X-STOODERS!

Привет, {message.from_user.first_name}!
Выберите интересующую вас категорию товаров:
"""

    await message.answer(
        welcome_text,
        reply_markup=await get_main_menu()
    )

@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery):
    welcome_text = """
🛍 X-STOODERS - Главное меню

Выберите интересующую вас категорию товаров:
"""

    await callback.message.edit_text(
        welcome_text,
        reply_markup=await get_main_menu()
    )

@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    from keyboards.main_menu import get_back_to_menu

    await callback.message.edit_text(
        FAQ_TEXT,
        reply_markup=get_back_to_menu()
    )