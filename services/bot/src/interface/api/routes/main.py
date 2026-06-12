# packages

from aiogram import (
    Router,
    F,
)

from aiogram.types import CallbackQuery

# application depencies

from ..dto.callback import NavigationCD

from ..views import MainView


main_router = Router()


@main_router.callback_query(NavigationCD.filter(F.level == "main"))
async def show_main_menu(
    callback: CallbackQuery,
) -> None:
    text, builder = MainView.build()

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
    )
    await callback.answer()
