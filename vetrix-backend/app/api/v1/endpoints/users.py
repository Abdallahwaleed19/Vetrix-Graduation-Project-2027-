from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import RequireRole, get_db
from app.core.security import get_password_hash
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (Admin only)",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole(["admin"])),
) -> User:
    """Create a new user in the system. Strictly restricted to admin users."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists in the system.",
        )

    role = db.query(Role).filter(Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {user_in.role_id} does not exist.",
        )

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role_id=user_in.role_id,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Maintain user_roles junction mapping per ERD specification
    user_role_entry = UserRole(user_id=user.id, role_id=user.role_id)
    db.add(user_role_entry)
    db.commit()

    return user


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List system users (Admin & Supervisor only)",
)
def read_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Number of records to return"),
    current_user: User = Depends(RequireRole(["admin", "supervisor"])),
) -> List[User]:
    """Retrieve users list. Restricted to users with 'admin' or 'supervisor' role."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users
