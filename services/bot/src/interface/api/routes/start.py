# packages

from aiogram import Router

from aiogram.filters import Command

from aiogram.types import Message

# application depencies

from ..views import MainView


start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(
    message: Message,
) -> None:
    text, builder = MainView.build()

    await message.answer(
        text,
        reply_markup=builder.as_markup(),
    )
