from http import HTTPStatus

from fastapi import HTTPException

from app.models import CharityProject
from app.core.db import AsyncSession
from app.crud.charity_project import charity_project_crud


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка на уникальность названия сбора"""
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_before_edit(
        project_id: id,
        session: AsyncSession
) -> CharityProject:
    """Проверка перед редактированием"""
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Сбор не найден!')
    if project.close_date:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'Закрытый проект нельзя редактировать!'
        )
    return project


async def check_project_before_delete(
        project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка перед удалением"""
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'В проект были внесены средства, не подлежит удалению!'
        )
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            'В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_amount_is_more_than_donated(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession
) -> None:
    """Проверка, что изменяемый сбор больше, чем уже собранная сумма"""
    project = await charity_project_crud.get(project_id, session)
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            'Новая сумма сбора должна быть больше той, что уже набрана!'
        )
