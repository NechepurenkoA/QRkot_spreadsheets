from fastapi import APIRouter, Depends

from app.models import User
from app.core.db import AsyncSession, get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationMyDB,
    DonationForAdminDB,
    DonationCreate
)
from app.services.investments import invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationForAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Возвр. ВСЕ донаты, только для супер-юзера"""
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    '/',
    response_model=DonationMyDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def donate(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Отправить 'донат'"""
    donation = await donation_crud.create(donation, session, user)
    await invest(session)
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=list[DonationMyDB],
    dependencies=[Depends(current_user)]
)
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Возвращает все донаты пользователя"""
    donations = await donation_crud.get_user_donations(user, session)
    return donations
