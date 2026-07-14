# Project: Titan Cloud Tech (Support Bot API)
# Path: core/utils/settings.py
# Compliance: PROJECT_DNA_V6.5 (Pydantic-Based Config)

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройки загрузки .env файла именно для проекта поддержки
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Игнорируем всё лишнее
    )

    # --- [ TELEGRAM SUPPORT BOT ] ---
    TG_SUPPORT_BOT_NAME: str
    TG_SUPPORT_BOT_TOKEN: str

    # --- [ TELEGRAM ADMIN GROUP & TOPICS ] ---
    TG_ADMIN_GROUP_ID: int     # ID группы (начинается с -100)
    TG_TOPIC_SUPPORT_ID: int   # ID темы "Саппорт"
    TG_TOPIC_LOGS_ID: int      # ID темы "Логи / Ошибки" (бывший General)

    # --- [ VALIDATION ] ---
    @field_validator("TG_SUPPORT_BOT_TOKEN", mode="before")
    @classmethod
    def check_support_token(cls, value):
        if not value:
            print("⚠️ Внимание: TG_SUPPORT_BOT_TOKEN отсутствует. Бот поддержки не запустится.")
        return value


# Инициализируем синглтон конфигурации для проекта поддержки
settings = Settings()