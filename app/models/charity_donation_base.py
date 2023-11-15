from datetime import datetime as dt

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean
)

from app.core.db import Base


class CharityDonationBase(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime)
