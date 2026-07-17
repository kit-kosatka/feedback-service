from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=5, max_length=20)
    email: EmailStr
    comment: str = Field(min_length=10, max_length=2000)


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    sentiment: str | None
    email_sent: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
