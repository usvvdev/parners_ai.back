# packages

from aiogram import Bot

from aiogram.fsm.context import FSMContext

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
)

from .filter_state import clear_state_keep_filters


async def delete_message_safe(
    bot: Bot,
    chat_id: int,
    message_id: int,
) -> None:
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )
    except Exception:
        pass


async def init_form_context(
    state: FSMContext,
    callback: CallbackQuery,
    **extra,
) -> None:
    await clear_state_keep_filters(state)
    await state.update_data(
        chat_id=callback.message.chat.id,
        menu_message_id=callback.message.message_id,
        **extra,
    )


async def edit_menu_message(
    bot: Bot,
    state: FSMContext,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    data = await state.get_data()

    await bot.edit_message_text(
        text=text,
        chat_id=data["chat_id"],
        message_id=data["menu_message_id"],
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


async def delete_user_message(message: Message) -> None:
    await delete_message_safe(
        message.bot,
        message.chat.id,
        message.message_id,
    )


async def render_callback(
    callback: CallbackQuery,
    text: str,
    builder,
    *,
    answer: str | None = None,
) -> None:
    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer(answer or "")
