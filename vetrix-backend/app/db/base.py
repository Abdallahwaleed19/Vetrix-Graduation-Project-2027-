"""Declarative Base aggregator for Alembic autogenerate discovery."""
from app.db.session import Base
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole

__all__ = ["Base", "Role", "User", "UserRole"]
