from io import BytesIO

import requests
import easyocr
from rapidfuzz import process

reader = easyocr.Reader(["ru", "en"])


def match_logo_to_offer(image_url: str, offer_names: list[str]):
    image_bytes = requests.get(image_url).content

    result = reader.readtext(image_bytes, detail=0)

    detected_text = " ".join(result)

    best_match, score, _ = process.extractOne(
        detected_text,
        offer_names,
    )

    return best_match, score, detected_text


offer = match_logo_to_offer(
    "https://365zaim.ru/images/zarybas.png",
    [
        "Зарубас",
        "Магнит",
        "Пятёрочка",
    ],
)

print(offer)
