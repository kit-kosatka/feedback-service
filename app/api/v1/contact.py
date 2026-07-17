from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.rate_limit import check_rate_limit
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import ContactService

router = APIRouter(prefix="/api", tags=["contact"])


@router.post(
    "/contact",
    response_model=ContactResponse,
    status_code=201,
    dependencies=[Depends(check_rate_limit)],
)
async def create_contact(
    data: ContactCreate,
    db: AsyncSession = Depends(get_db),
) -> ContactResponse:
    service = ContactService(db)
    contact = await service.process_contact_request(data)
    return ContactResponse.model_validate(contact)