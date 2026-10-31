import sys
from contextlib import asynccontextmanager
from typing import Generator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole

DEFAULT_ROLES = [
    {
        "name": "admin",
        "description": "System Administrator with full access to manage users, roles, and CFR 21 compliance logs",
    },
    {
        "name": "analyst",
        "description": "Laboratory Analyst executing bench testing, instrument calibration, and sample measurement data entry",
    },
    {
        "name": "reviewer",
        "description": "Technical Reviewer performing data verification, spec validation, and preliminary test review",
    },
    {
        "name": "supervisor",
        "description": "Laboratory Supervisor authorizing Certificate of Analysis (CoA), user oversight, and OOS closures",
    },
]


def init_db(db: Session) -> None:
    """Populate default initial roles and a default administrator user if absent."""
    # Seed roles
    for role_item in DEFAULT_ROLES:
        role = db.query(Role).filter(Role.name == role_item["name"]).first()
        if not role:
            new_role = Role(
                name=role_item["name"],
                description=role_item["description"],
            )
            db.add(new_role)
    db.commit()

    # Seed initial default admin if no users exist
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if admin_role:
        existing_admin = db.query(User).filter(User.email == "admin@vetrix.lims").first()
        if not existing_admin:
            admin_user = User(
                email="admin@vetrix.lims",
                hashed_password=get_password_hash("Admin123!"),
                full_name="Default System Administrator",
                role_id=admin_role.id,
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            # Assign user_roles junction per ERD
            admin_user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db.add(admin_user_role)
            db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI application lifespan handler."""
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Configure CORS Middleware for development & front-end clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router aggregator
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"], summary="System health check endpoint")
def health_check():
    """Health check endpoint to verify backend operational readiness."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "api_prefix": settings.API_V1_STR,
    }


@app.get("/", tags=["Health"], include_in_schema=False)
def root_redirect():
    """Root redirect / information endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs_url": f"{settings.API_V1_STR}/docs",
        "openapi_url": f"{settings.API_V1_STR}/openapi.json",
    }


def cli_seed():
    """Standalone CLI entry point to seed roles and initial administrator."""
    print("Connecting to database...")
    with SessionLocal() as db:
        print("Seeding initial roles: 'admin', 'analyst', 'reviewer', 'supervisor'...")
        init_db(db)
        print("Seeding completed successfully.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "seed":
        cli_seed()
    else:
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
