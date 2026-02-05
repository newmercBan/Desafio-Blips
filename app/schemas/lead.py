from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: str
    birth_date: Optional[str] = None

    class Config:
        # Allow population from MongoDB objects
        populate_by_name = True
