import logging

from groq import Groq

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
client = Groq(api_key=settings.groq_api_key)


async def analyze_sentiment(comment: str) -> str | None:
    """
    Определяет тональность комментария: positive / neutral / negative.
    При любой ошибке возвращает None (fallback), не роняя сервис.
    """
    try:
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты классификатор тональности текста. "
                        "Ответь ровно одним словом: positive, neutral или negative."
                    ),
                },
                {"role": "user", "content": comment},
            ],
            max_tokens=5,
            temperature=0,
        )
        result = response.choices[0].message.content.strip().lower().rstrip(".!")

        if result not in {"positive", "neutral", "negative"}:
            logger.warning("AI вернул неожиданный ответ: %s", result)
            return None

        return result

    except Exception:
        logger.exception("Ошибка при обращении к AI (Groq), продолжаем без sentiment")
        return None
