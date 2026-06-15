# packages

from langchain_core.messages import HumanMessage

from langchain_google_genai import ChatGoogleGenerativeAI

from libs.core.config import TApplicationConfig
from libs.core.constants import SYSTEM_PROMPT

from ....domain.protocols import IGeminiProtocol
from ....domain.types._types import PartnerResult
from libs.domain.types._types.shared import ImagePayload


class Gemini(IGeminiProtocol):
    def __init__(
        self,
        config: type[TApplicationConfig],
    ) -> None:
        self._client = ChatGoogleGenerativeAI(
            model=config.google_model,
            temperature=1.0,
            api_key=config.google_api_key,
            client_args={
                "proxy": config.proxy_url,
            },
        )

    async def analyze(
        self,
        *,
        screenshot: str,
        markdown: str,
        showcase_url: str,
        target_offers: list[str],
    ) -> PartnerResult:
        image_payload = ImagePayload(
            value=screenshot,
        )

        prompt = SYSTEM_PROMPT.format(
            showcase_url=showcase_url,
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
            ],
        )

        llm = self._client.with_structured_output(
            PartnerResult,
        )

        return await llm.ainvoke(
            [message],
        )
