# packages

from aiogram import Router

from aiogram.filters import Command

from aiogram.types import Message

# application dependencies

from ..utils import get_main_menu


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    text, markup = get_main_menu()

    await message.answer(
        text,
        reply_markup=markup,
    )
