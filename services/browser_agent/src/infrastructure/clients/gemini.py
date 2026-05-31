# packages

from httpx import Client

from langchain_core.messages import HumanMessage

from langchain_google_genai import ChatGoogleGenerativeAI

# application dependencies

from libs.core.config import TApplicationConfig

from ...domain.types import PartnerResult

from libs.core.constants import SYSTEM_PROMPT

from ...domain.protocols import IGeminiProtocol

from libs.domain.types._types.shared import ImagePayload


class Gemini(IGeminiProtocol):
    def __init__(
        self,
        config: type[TApplicationConfig],
    ) -> None:
        self._config = config

        self._client = ChatGoogleGenerativeAI(
            model=self._config.google_model,
            temperature=1.0,
            api_key=self._config.google_api_key,
            httpx_client=Client(
                proxy=self._config.proxy_url,
            ),
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
