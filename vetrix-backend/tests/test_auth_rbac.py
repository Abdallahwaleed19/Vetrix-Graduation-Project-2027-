import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import RequireRole, get_current_user
from app.api.v1.endpoints.auth import login_for_access_token, read_current_user
from app.api.v1.endpoints.users import create_user, read_users
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import Base
from app.main import init_db
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user import UserCreate

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create fresh database schema and yield session per test function."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    init_db(session)
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_password_hashing():
    password = "SecretPassword123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_create_access_token():
    token = create_access_token(subject=1, role="admin")
    assert isinstance(token, str)
    assert len(token) > 20


def test_seed_initial_roles_and_admin(db_session):
    roles = db_session.query(Role).all()
    role_names = [r.name for r in roles]
    assert "admin" in role_names
    assert "analyst" in role_names
    assert "reviewer" in role_names
    assert "supervisor" in role_names

    admin_user = db_session.query(User).filter(User.email == "admin@vetrix.lims").first()
    assert admin_user is not None
    assert admin_user.role.name == "admin"

    # Verify user_roles junction per ERD
    user_role_entry = db_session.query(UserRole).filter(UserRole.user_id == admin_user.id).first()
    assert user_role_entry is not None
    assert user_role_entry.role_id == admin_user.role_id


def test_login_endpoint_success(db_session):
    form_data = OAuth2PasswordRequestForm(
        username="admin@vetrix.lims",
        password="Admin123!",
        scope="",
        grant_type="password",
    )
    token_response = login_for_access_token(db=db_session, form_data=form_data)
    assert token_response.access_token is not None
    assert token_response.token_type == "bearer"


def test_login_endpoint_invalid_credentials(db_session):
    bad_form = OAuth2PasswordRequestForm(
        username="admin@vetrix.lims",
        password="WrongPassword!",
        scope="",
        grant_type="password",
    )
    with pytest.raises(HTTPException) as exc_info:
        login_for_access_token(db=db_session, form_data=bad_form)
    assert exc_info.value.status_code == 401
    assert "Incorrect email or password" in exc_info.value.detail


def test_get_current_user_dependency(db_session):
    admin = db_session.query(User).filter(User.email == "admin@vetrix.lims").first()
    token = create_access_token(subject=admin.id, role=admin.role.name)
    user = get_current_user(db=db_session, token=token)
    assert user.id == admin.id
    assert user.email == "admin@vetrix.lims"

    # Invalid token raises 401
    with pytest.raises(HTTPException) as exc:
        get_current_user(db=db_session, token="invalid.token.here")
    assert exc.value.status_code == 401


def test_read_current_user_me(db_session):
    admin = db_session.query(User).filter(User.email == "admin@vetrix.lims").first()
    result = read_current_user(current_user=admin)
    assert result.id == admin.id
    assert result.email == "admin@vetrix.lims"


def test_require_role_rbac_dependency(db_session):
    admin = db_session.query(User).filter(User.email == "admin@vetrix.lims").first()
    analyst_role = db_session.query(Role).filter(Role.name == "analyst").first()

    analyst_user = User(
        email="analyst@vetrix.lims",
        hashed_password=get_password_hash("Pass123!"),
        full_name="Lab Analyst",
        role_id=analyst_role.id,
        is_active=True,
    )
    db_session.add(analyst_user)
    db_session.commit()

    admin_checker = RequireRole(["admin"])
    supervisor_or_admin_checker = RequireRole(["admin", "supervisor"])

    # Admin is allowed for both
    assert admin_checker(current_user=admin) == admin
    assert supervisor_or_admin_checker(current_user=admin) == admin

    # Analyst is forbidden from admin checker -> raises 403
    with pytest.raises(HTTPException) as exc:
        admin_checker(current_user=analyst_user)
    assert exc.value.status_code == 403
    assert "Operation not permitted" in exc.value.detail


def test_create_user_admin_and_duplicate_check(db_session):
    admin = db_session.query(User).filter(User.email == "admin@vetrix.lims").first()
    analyst_role = db_session.query(Role).filter(Role.name == "analyst").first()

    payload = UserCreate(
        email="new_analyst@vetrix.lims",
        full_name="New Lab Analyst",
        password="SecurePassword123!",
        role_id=analyst_role.id,
    )

    created_user = create_user(user_in=payload, db=db_session, current_user=admin)
    assert created_user.id is not None
    assert created_user.email == "new_analyst@vetrix.lims"
    assert created_user.role_id == analyst_role.id

    # Verify UserRole junction table entry created per ERD
    junction = db_session.query(UserRole).filter(UserRole.user_id == created_user.id).first()
    assert junction is not None
    assert junction.role_id == analyst_role.id

    # Duplicate email raises 400
    with pytest.raises(HTTPException) as exc_dup:
        create_user(user_in=payload, db=db_session, current_user=admin)
    assert exc_dup.value.status_code == 400
    assert "already exists" in exc_dup.value.detail

    # Non-existent role raises 404
    bad_role_payload = UserCreate(
        email="bad_role@vetrix.lims",
        full_name="Bad Role User",
        password="Password123!",
        role_id=9999,
    )
    with pytest.raises(HTTPException) as exc_role:
        create_user(user_in=bad_role_payload, db=db_session, current_user=admin)
    assert exc_role.value.status_code == 404


def test_read_users_list(db_session):
    admin = db_session.query(User).filter(User.email == "admin@vetrix.lims").first()
    users = read_users(db=db_session, skip=0, limit=100, current_user=admin)
    assert len(users) >= 1
    assert any(u.email == "admin@vetrix.lims" for u in users)
