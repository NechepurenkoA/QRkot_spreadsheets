from sqlalchemy import (
    Column,
    String,
    Text
)

from app.models.charity_donation_base import CharityDonationBase


class CharityProject(CharityDonationBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text(), nullable=False)
