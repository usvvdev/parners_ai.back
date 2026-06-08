import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


# --- Фабрики CallbackData для навигации ---
class NavCD(CallbackData, prefix="nav"):
    level: str


class PartnerCD(CallbackData, prefix="prt"):
    action: str
    p_id: int


class LinkCD(CallbackData, prefix="lnk"):
    action: str
    p_id: int
    l_id: int


class OfferCD(CallbackData, prefix="off"):
    action: str
    p_id: int
    l_id: int
    o_id: int


# --- Взаимодействие с реальным API ---


async def fetch_partners():
    """Асинхронно получает реальные данные с твоего API."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Ошибка API: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"Ошибка соединения с API: {e}")
            return []


async def update_api_status(endpoint: str, item_id: int, payload: dict):
    """
    Отправляет PATCH запрос на сервер для изменения данных.
    endpoint: 'partners', 'links' или 'offers' (зависит от твоего бекенда)
    """
    # Пример URL: https://dydex.ru/api/partners/1/
    url = f"https://dydex.ru/api/{endpoint}/{item_id}/"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(url, json=payload) as response:
                if response.status in (200, 204):
                    return True
                else:
                    logging.error(f"Ошибка обновления API: {response.status}")
                    return False
        except Exception as e:
            logging.error(f"Ошибка отправки данных: {e}")
            return False


# --- Хэндлеры ---


@router.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="📂 Список партнеров", callback_data=NavCD(level="partners"))
    await message.answer(
        "👋 Добро пожаловать в CRM!\nВыберите действие:",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(NavCD.filter(F.level == "partners"))
async def show_partners(callback: CallbackQuery):
    partners = await fetch_partners()

    if not partners:
        return await callback.answer(
            "Список партнеров пуст или API недоступен", show_alert=True
        )

    builder = InlineKeyboardBuilder()
    for p in partners:
        status = "🟢" if p.get("is_tracking") else "🔴"
        builder.button(
            text=f"{status} {p['title']}",
            callback_data=PartnerCD(action="view", p_id=p["id"]),
        )

    builder.adjust(1)
    await callback.message.edit_text(
        "📂 **Список партнеров:**",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown",
    )


@router.callback_query(PartnerCD.filter(F.action == "view"))
async def show_partner(callback: CallbackQuery, callback_data: PartnerCD):
    partners = await fetch_partners()
    partner = next((p for p in partners if p["id"] == callback_data.p_id), None)

    if not partner:
        return await callback.answer("Партнер не найден!")

    builder = InlineKeyboardBuilder()

    t_text = (
        "🔕 Выключить трекинг" if partner.get("is_tracking") else "🔔 Включить трекинг"
    )
    builder.button(
        text=t_text, callback_data=PartnerCD(action="toggle", p_id=partner["id"])
    )

    for link in partner.get("links", []):
        status = "🟢" if link.get("is_active") else "🔴"
        short_url = link["link"].replace("https://", "").replace("http://", "")[:20]
        builder.button(
            text=f"{status} {short_url}...",
            callback_data=LinkCD(action="view", p_id=partner["id"], l_id=link["id"]),
        )

    builder.button(text="🔙 Назад к партнерам", callback_data=NavCD(level="partners"))
    builder.adjust(1)

    await callback.message.edit_text(
        f"🏢 **Партнер:** {partner['title']}\n"
        f"📊 **Трекинг:** {'Активен' if partner.get('is_tracking') else 'Выключен'}\n\n"
        f"🔗 **Доступные ссылки ({len(partner.get('links', []))} шт.):**",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown",
    )


@router.callback_query(LinkCD.filter(F.action == "view"))
async def show_link(callback: CallbackQuery, callback_data: LinkCD):
    partners = await fetch_partners()
    partner = next((p for p in partners if p["id"] == callback_data.p_id), None)
    link = (
        next((l for l in partner["links"] if l["id"] == callback_data.l_id), None)
        if partner
        else None
    )

    if not link:
        return await callback.answer("Ссылка не найдена!")

    builder = InlineKeyboardBuilder()

    l_text = (
        "❌ Деактивировать ссылку"
        if link.get("is_active")
        else "✅ Активировать ссылку"
    )
    builder.button(
        text=l_text,
        callback_data=LinkCD(action="toggle", p_id=partner["id"], l_id=link["id"]),
    )

    for offer in link.get("offers", []):
        status = "🟢" if offer.get("is_active") else "🔴"
        builder.button(
            text=f"{status} {offer['title']}",
            callback_data=OfferCD(
                action="view", p_id=partner["id"], l_id=link["id"], o_id=offer["id"]
            ),
        )

    builder.button(
        text="🔙 Назад к партнеру",
        callback_data=PartnerCD(action="view", p_id=partner["id"]),
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"🔗 Ссылка:\n"
        f"⚡ **Статус:** {'Активна' if link.get('is_active') else 'Отключена'}\n\n"
        f"🎁 **Офферы этой ссылки ({len(link.get('offers', []))} шт.):**",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


@router.callback_query(OfferCD.filter(F.action == "view"))
async def show_offer(callback: CallbackQuery, callback_data: OfferCD):
    partners = await fetch_partners()
    partner = next((p for p in partners if p["id"] == callback_data.p_id), None)
    link = (
        next((l for l in partner["links"] if l["id"] == callback_data.l_id), None)
        if partner
        else None
    )
    offer = (
        next((o for o in link["offers"] if o["id"] == callback_data.o_id), None)
        if link
        else None
    )

    if not offer:
        return await callback.answer("Оффер не найден!")

    builder = InlineKeyboardBuilder()

    o_text = "🔴 Выключить оффер" if offer.get("is_active") else "🟢 Включить оффер"
    builder.button(
        text=o_text,
        callback_data=OfferCD(
            action="toggle",
            p_id=callback_data.p_id,
            l_id=callback_data.l_id,
            o_id=offer["id"],
        ),
    )

    builder.button(
        text="🔙 Назад к ссылке",
        callback_data=LinkCD(
            action="view", p_id=callback_data.p_id, l_id=callback_data.l_id
        ),
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"🎁 **Оффер:** {offer['title']}\n"
        f"🆔 **ID:** {offer['id']}\n"
        f"⚡ **Статус:** {'Активен' if offer.get('is_active') else 'Неактивен'}",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown",
    )


# --- Обработчики изменения статусов (Toggle) с реальными запросами ---


@router.callback_query(PartnerCD.filter(F.action == "toggle"))
async def toggle_partner(callback: CallbackQuery, callback_data: PartnerCD):
    partners = await fetch_partners()
    partner = next((p for p in partners if p["id"] == callback_data.p_id), None)
    if not partner:
        return await callback.answer("Ошибка!")

    new_status = not partner.get("is_tracking")

    # Отправляем PATCH запрос на сервер
    success = await update_api_status(
        "partners", callback_data.p_id, {"is_tracking": new_status}
    )

    if success:
        await callback.answer(f"Трекинг {'включен' if new_status else 'выключен'}!")
    else:
        await callback.answer("Не удалось обновить статус на сервере", show_alert=True)

    callback_data.action = "view"
    await show_partner(callback, callback_data)


@router.callback_query(LinkCD.filter(F.action == "toggle"))
async def toggle_link(callback: CallbackQuery, callback_data: LinkCD):
    partners = await fetch_partners()
    partner = next((p for p in partners if p["id"] == callback_data.p_id), None)
    link = (
        next((l for l in partner["links"] if l["id"] == callback_data.l_id), None)
        if partner
        else None
    )
    if not link:
        return await callback.answer("Ошибка!")

    new_status = not link.get("is_active")

    # Отправляем PATCH запрос
    success = await update_api_status(
        "links", callback_data.l_id, {"is_active": new_status}
    )

    if success:
        await callback.answer(
            f"Ссылка {'активирована' if new_status else 'деактивирована'}!"
        )
    else:
        await callback.answer("Не удалось обновить статус на сервере", show_alert=True)

    callback_data.action = "view"
    await show_link(callback, callback_data)


@router.callback_query(OfferCD.filter(F.action == "toggle"))
async def toggle_offer(callback: CallbackQuery, callback_data: OfferCD):
    partners = await fetch_partners()
    partner = next((p for p in partners if p["id"] == callback_data.p_id), None)
    link = (
        next((l for l in partner["links"] if l["id"] == callback_data.l_id), None)
        if partner
        else None
    )
    offer = (
        next((o for o in link["offers"] if o["id"] == callback_data.o_id), None)
        if link
        else None
    )
    if not offer:
        return await callback.answer("Ошибка!")

    new_status = not offer.get("is_active")

    # Отправляем PATCH запрос
    success = await update_api_status(
        "offers", callback_data.o_id, {"is_active": new_status}
    )

    if success:
        await callback.answer(f"Оффер {'включен' if new_status else 'выключен'}!")
    else:
        await callback.answer("Не удалось обновить статус на сервере", show_alert=True)

    callback_data.action = "view"
    await show_offer(callback, callback_data)


# --- Запуск ---
async def run_app():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    asyncio.run(run_app())


if __name__ == "__main__":
    main()
