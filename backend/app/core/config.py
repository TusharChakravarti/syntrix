from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings:
    app_name: str = "Syntrix"
    app_version:str = "1.0.0"
    debug:bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()