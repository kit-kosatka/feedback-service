import logging

import resend

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
resend.api_key = settings.resend_api_key


async def send_contact_emails(
    name: str, email: str, comment: str, sentiment: str | None
) -> bool:
    """
    Отправляет письмо владельцу сайта и копию пользователю.
    При ошибке возвращает False (fallback), не роняя сервис.
    """
    try:
        resend.Emails.send(
            {
                "from": settings.email_from,
                "to": settings.owner_email,
                "subject": f"Новое обращение от {name}",
                "html": (
                    f"<p><b>Имя:</b> {name}</p>"
                    f"<p><b>Email:</b> {email}</p>"
                    f"<p><b>Тональность:</b> {sentiment or 'не определена'}</p>"
                    f"<p><b>Комментарий:</b> {comment}</p>"
                ),
            }
        )

        resend.Emails.send(
            {
                "from": settings.email_from,
                "to": email,
                "subject": "Мы получили ваше обращение",
                "html": (
                    f"<p>Здравствуйте, {name}!</p>"
                    f"<p>Спасибо за обращение, мы скоро с вами свяжемся.</p>"
                ),
            }
        )

        return True

    except Exception:
        logger.exception("Ошибка при отправке email через Resend")
        return False
