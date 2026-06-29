# packages

from dataclasses import dataclass
from html import escape

import httpx

from loguru import logger

# application dependencies

from libs.domain.types._types.options import TelegramOptions
from libs.domain.types.enums.config import UserRole


@dataclass(frozen=True)
class OfferPositionChange:
    wmid: str
    utm_source: str
    vitrina: str
    offer: str
    previous_position: int
    current_position: int


class NotificationService:
    def __init__(
        self,
        *,
        telegram_options: TelegramOptions | None,
        proxy_url: str | None = None,
    ) -> None:
        self._telegram_options = telegram_options
        self._client = httpx.AsyncClient(
            proxy=proxy_url,
            timeout=10.0,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    def _recipient_ids(self) -> list[int]:
        if not self._telegram_options:
            return []

        users = self._telegram_options.allowed_users.root

        return [
            int(user_id)
            for user_id, options in users.items()
            if options.role == UserRole.MARKETING and options.notifications
        ]

    def _build_position_change_text(
        self,
        change: OfferPositionChange,
    ) -> str:
        delta = change.previous_position - change.current_position
        sign = "📈" if delta > 0 else "📉"

        delta_block = f"{sign} <b>Изменение:</b> {abs(delta)} позиций\n\n"

        return (
            "📊 <b>Позиция оффера изменилась</b>\n\n"
            f"🏷 <b>Оффер:</b> {escape(change.offer)}\n"
            f"🏢 <b>WMID:</b> {escape(change.wmid)}\n"
            f"🔗 <b>Витрина:</b> {escape(change.vitrina)}\n"
            f"🌐 <b>UTM:</b> {escape(change.utm_source)}\n\n"
            f"{delta_block}"
            "📌 <b>Детали</b>\n"
            f"🏁 Было: <b>{change.previous_position}</b>\n"
            f"🎯 Стало: <b>{change.current_position}</b>\n\n"
            f"📊 Итог: <b>{'выросла' if change.current_position < change.previous_position else 'снизилась'}</b>\n\n"
            f'📈 <a href="{self._telegram_options.dashboard_url}?wmid={escape(change.wmid)}&utm_source={escape(change.utm_source)}&offer={escape(change.offer)}">'
            "Открыть график</a>"
        )

    async def send_offer_position_changed(
        self,
        change: OfferPositionChange,
    ) -> None:
        if not self._telegram_options or not self._telegram_options.bot_token:
            logger.warning("Telegram bot token is not configured; skip notification")
            return

        text = self._build_position_change_text(change)

        endpoint = f"https://api.telegram.org/bot{self._telegram_options.bot_token}/sendMessage"

        payload = {
            "chat_id": self._telegram_options.chat_options.group_chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        # 👇 вот это главное
        if self._telegram_options.chat_options.topic_id:
            payload["message_thread_id"] = self._telegram_options.chat_options.topic_id

        try:
            response = await self._client.post(endpoint, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as err:
            logger.warning("Failed to send notification: {}", err)
