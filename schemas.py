from pydantic import BaseModel
from typing import Optional


class ItemCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: str


class ItemRead(ItemCreate):
    id: Optional[int] = None