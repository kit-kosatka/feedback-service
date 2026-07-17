import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactRequest
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate
from app.services.ai_service import analyze_sentiment
from app.services.email_service import send_contact_emails

logger = logging.getLogger(__name__)


class ContactService:
    def __init__(self, session: AsyncSession) -> None:
        self._repository = ContactRepository(session)

    async def process_contact_request(self, data: ContactCreate) -> ContactRequest:
        logger.info("Новое обращение от %s (%s)", data.name, data.email)

        sentiment = await analyze_sentiment(data.comment)

        email_sent = await send_contact_emails(
            name=data.name,
            email=data.email,
            comment=data.comment,
            sentiment=sentiment,
        )

        contact = ContactRequest(
            name=data.name,
            phone=data.phone,
            email=data.email,
            comment=data.comment,
            sentiment=sentiment,
            email_sent=email_sent,
        )

        return await self._repository.create(contact)
