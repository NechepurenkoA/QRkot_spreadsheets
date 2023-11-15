from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


class CRUDMeetingRoom(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):

    @staticmethod
    async def get_project_id_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Объект CharityProject по имени"""
        project_id = await session.scalars(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_id = project_id.first()
        return project_id


charity_project_crud = CRUDMeetingRoom(CharityProject)
