from fastapi import APIRouter, Depends

from app.api.validators import (
    check_project_name_duplicate,
    check_project_before_edit,
    check_amount_is_more_than_donated,
    check_project_before_delete
)
from app.core.db import AsyncSession, get_async_session
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investments import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвр. все сборы"""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создать сбор, только для супер-пользователя"""
    await check_project_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await invest(session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def patch_charity_project(
        obj_in: CharityProjectUpdate,
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Отредактировать сбор, только для супер-пользователя"""
    project = await check_project_before_edit(
        project_id,
        session
    )
    if obj_in.name is not None:
        await check_project_name_duplicate(
            obj_in.name, session
        )
    if obj_in.full_amount is not None:
        await check_amount_is_more_than_donated(
            project_id, obj_in.full_amount, session
        )
    new_project = await charity_project_crud.update(
        project,
        obj_in,
        session
    )
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удалить сбор, только для супер-пользователя"""
    project = await check_project_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project
