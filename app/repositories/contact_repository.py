from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactRequest


class ContactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, contact: ContactRequest) -> ContactRequest:
        self._session.add(contact)
        await self._session.commit()
        await self._session.refresh(contact)
        return contact

    async def get_by_id(self, contact_id: int) -> ContactRequest | None:
        result = await self._session.execute(
            select(ContactRequest).where(ContactRequest.id == contact_id)
        )
        return result.scalar_one_or_none()

    async def count_all(self) -> int:
        result = await self._session.execute(select(ContactRequest))
        return len(result.scalars().all())

    async def count_by_sentiment(self, sentiment: str) -> int:
        result = await self._session.execute(
            select(ContactRequest).where(ContactRequest.sentiment == sentiment)
        )
        return len(result.scalars().all())
