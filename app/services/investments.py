from datetime import datetime as dt

from sqlalchemy import select

from app.models import Donation, CharityProject
from app.core.db import AsyncSession


QUERY_PARAM = False


async def close_donation_or_project(
        to_close: Donation or CharityProject
) -> None:
    """Фун-ия для закрытия доната или проэкта сбора"""
    to_close.fully_invested = True
    to_close.close_date = dt.now()


async def investment_addition(
        project: CharityProject,
        donation: Donation,
        to_add: int
) -> None:
    """Фун-ия 'распределитель'"""
    project.invested_amount += to_add
    donation.invested_amount += to_add


async def add_donation_to_project(
        donation: Donation,
        project: CharityProject
):
    """Фун-ия для распределения средств"""
    project_difference: int = (
        project.full_amount - project.invested_amount
    )  # разность между целью и собранными деньгами
    donation_difference: int = (
        donation.full_amount - donation.invested_amount
    )  # разность между пожертвованными и уже распределенными деньгами

    if project_difference >= donation_difference:
        await investment_addition(project, donation, donation_difference)

    if project_difference < donation_difference:
        await investment_addition(project, donation, project_difference)

    if project.invested_amount == project.full_amount:
        await close_donation_or_project(project)

    if donation.invested_amount == donation.full_amount:
        await close_donation_or_project(donation)

    return project


async def invest(session: AsyncSession) -> None:
    """Main фун-ия инвестирования"""
    projects_query = await session.scalars(
        select(CharityProject).where(CharityProject.fully_invested == QUERY_PARAM)
    )
    donations_query = await session.scalars(
        select(Donation).where(Donation.fully_invested == QUERY_PARAM)
    )
    uninvested_projects = projects_query.all()
    uninvested_donations = donations_query.all()
    for proj in uninvested_projects:
        for dono in uninvested_donations:
            proj = await add_donation_to_project(dono, proj)
            if proj.invested_amount == proj.full_amount:
                break
    await session.commit()
