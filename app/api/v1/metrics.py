from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.contact_repository import ContactRepository

router = APIRouter(prefix="/api", tags=["metrics"])


@router.get("/metrics")
async def get_metrics(db: AsyncSession = Depends(get_db)) -> dict[str, int]:
    repository = ContactRepository(db)

    return {
        "total_requests": await repository.count_all(),
        "positive": await repository.count_by_sentiment("positive"),
        "neutral": await repository.count_by_sentiment("neutral"),
        "negative": await repository.count_by_sentiment("negative"),
    }
