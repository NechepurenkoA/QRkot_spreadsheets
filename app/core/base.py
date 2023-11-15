"""Импорт моделей для генерации миграций с помощью Alembic"""
from app.core.db import Base  # noqa
from app.models import User, CharityProject, Donation  # noqa
