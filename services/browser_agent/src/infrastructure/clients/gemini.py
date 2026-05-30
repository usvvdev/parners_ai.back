# packages

import os

from langchain_core.messages import HumanMessage

from langchain_google_genai import ChatGoogleGenerativeAI

# application dependencies

from libs.core.config import TApplicationConfig

from src.domain.types import PartnerResult

from libs.core.constants import SYSTEM_PROMPT

from src.domain.protocols import IGeminiProtocol

from libs.domain.types._types.shared import ImagePayload


class Gemini(IGeminiProtocol):
    def __init__(
        self,
        # config: type[TApplicationConfig],
    ) -> None:
        # self._config = config

        self._client = ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL"),
            temperature=1.0,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )

    async def analyze(
        self,
        *,
        screenshot: str,
        markdown: str,
        target_offers: list[str],
    ) -> PartnerResult:

        image_payload = ImagePayload(
            value=screenshot,
        )

        prompt: str = SYSTEM_PROMPT.format(
            target_offers=", ".join(target_offers),
            markdown=markdown[:50000],
        )

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_payload.value,
                    },
                },
            ]
        )

        llm = self._client.with_structured_output(
            PartnerResult,
        )

        return await llm.ainvoke(
            [message],
        )
