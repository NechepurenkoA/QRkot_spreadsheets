from datetime import datetime
from typing import Optional


from pydantic import (
    BaseModel,
    PositiveInt,
    Extra
)


class DonationBase(BaseModel):
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationMyDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationForAdminDB(DonationMyDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
