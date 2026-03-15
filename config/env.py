from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DatabaseSettings(BaseAppSettings):
    """
    Настройки подключения к базе данных.
    Поддерживает SQLite и сетевые БД.
    """

    engine: str = Field(alias="DB_ENGINE")
    name: str = Field(alias="DB_NAME")

    host: str | None = Field(default=None, alias="DB_HOST")
    port: int | None = Field(default=None, alias="DB_PORT")
    user: str | None = Field(default=None, alias="DB_USER")
    password: str | None = Field(default=None, alias="DB_PASSWORD")

    @property
    def django_config(self) -> dict:
        if self.engine == "django.db.backends.sqlite3":
            return {
                "ENGINE": self.engine,
                "NAME": str(BASE_DIR / self.name),
            }

        return {
            "ENGINE": self.engine,
            "NAME": self.name,
            "USER": self.user,
            "PASSWORD": self.password,
            "HOST": self.host,
            "PORT": self.port,
        }


class DjangoSettings(BaseAppSettings):
    secret_key: Annotated[str, Field(alias="SECRET_KEY")]
    debug: bool = Field(default=False, alias="DEBUG")
    allowed_hosts: list[str] = Field(default_factory=list, alias="ALLOWED_HOSTS")


class Settings(BaseAppSettings):
    django: DjangoSettings = DjangoSettings()
    database: DatabaseSettings = DatabaseSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
