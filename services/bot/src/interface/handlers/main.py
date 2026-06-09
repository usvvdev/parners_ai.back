# packages

from aiogram import Router, F

from aiogram.types import CallbackQuery

# application dependencies

from ..utils import get_main_menu

from ..callbacks import NavCD


router = Router()


@router.callback_query(NavCD.filter(F.level == "main"))
async def show_main_menu(callback: CallbackQuery):
    text, markup = get_main_menu()

    await callback.message.edit_text(
        text,
        reply_markup=markup,
    )
    await callback.answer()
