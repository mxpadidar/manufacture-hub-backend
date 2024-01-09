from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    debug: bool = True

    postgres_driver: str = "postgresql+psycopg"
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"

    @property
    def database_url(self) -> str:
        url = f"{self.postgres_driver}://\
                {self.postgres_user}:{self.postgres_password}@\
                {self.postgres_host}:{self.postgres_port}/\
                {self.postgres_db}"
        return url.replace(" ", "")

    model_config = SettingsConfigDict(
        env_file=base_dir / ".env",
        env_file_encoding="utf-8",
    )


configs = Config()
