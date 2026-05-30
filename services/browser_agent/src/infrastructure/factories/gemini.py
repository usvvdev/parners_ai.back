from ..clients.gemini import Gemini


class GeminiFactory:
    @staticmethod
    def create(
        config="",
    ) -> Gemini:
        return Gemini(
            config=config,
        )
