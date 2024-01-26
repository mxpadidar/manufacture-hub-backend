from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    debug: bool = True
    secret_key: str = "secret"

    postgres_driver: str = "postgresql+psycopg"
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"

    jwt_access_token_expire_seconds: int = 60 * 60
    jwt_refresh_token_expire_seconds: int = 60 * 60 * 24
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=base_dir / ".env",
        env_file_encoding="utf-8",
    )


envs = Envs()
