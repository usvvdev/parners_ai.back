# packages

from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    bot_token: str = Field(
        ...,
        description="Telegram Bot API token",
    )

    api_base_url: str = Field(
        default="http://localhost:8000/api",
        description="Base URL of the API service",
    )

    model_config = SettingsConfigDict(
        extra="ignore",
    )
