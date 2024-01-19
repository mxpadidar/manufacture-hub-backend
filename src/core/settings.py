from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    debug: bool = True

    postgres_driver: str = "postgresql+psycopg"
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"

    secret_key: str = "secret"
    jwt_expires_in_seconds: int = 1800
    jwt_algorithm: str = "HS256"
    token_url: str = "/accounts/login"

    @property
    def postgres_uri(self) -> str:
        url = f"{self.postgres_driver}://\
                {self.postgres_user}:{self.postgres_password}@\
                {self.postgres_host}:{self.postgres_port}/\
                {self.postgres_db}"
        return url.replace(" ", "")

    @property
    def jwt_expires_in(self) -> timedelta:
        expires_in = self.jwt_expires_in_seconds or 30 * 60
        return timedelta(seconds=expires_in)

    model_config = SettingsConfigDict(
        env_file=base_dir / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
