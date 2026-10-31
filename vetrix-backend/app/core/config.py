from typing import Optional
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings managed through environment variables."""

    PROJECT_NAME: str = "Vetrix LIMS Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super_secret_jwt_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "vetrix_db"
    POSTGRES_PORT: int = 5432

    # Optional explicit override for testing, container networks, or in-memory DBs
    SQLALCHEMY_DATABASE_URI_OVERRIDE: Optional[str] = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Dynamically assemble PostgreSQL DSN."""
        if self.SQLALCHEMY_DATABASE_URI_OVERRIDE:
            return self.SQLALCHEMY_DATABASE_URI_OVERRIDE
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
