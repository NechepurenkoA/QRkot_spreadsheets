from sqlalchemy import select

from app.models import User, Donation
from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.schemas.donation import DonationCreate


class CRUDMeetingRoom(CRUDBase[
    Donation,
    DonationCreate,
    None
]):

    @staticmethod
    async def get_user_donations(user: User, session: AsyncSession):
        donations = await session.scalars(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.all()


donation_crud = CRUDMeetingRoom(Donation)
