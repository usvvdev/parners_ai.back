# packages

from aiogram import Router

from aiogram.filters import Command

from aiogram.types import Message

from aiogram.utils.keyboard import InlineKeyboardBuilder

# application dependencies

from ..callbacks import NavCD


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📂 Список партнеров",
        callback_data=NavCD(level="partners"),
    )

    await message.answer(
        "👋 Добро пожаловать в CRM!\nВыберите действие:",
        reply_markup=builder.as_markup(),
    )
