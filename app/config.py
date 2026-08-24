from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./etos.db"
    ecos_api_key: str = ""
    fred_api_key: str = ""
    trading_economics_api_key: str = ""
    app_timezone: str = "Asia/Seoul"
    minimum_score: int = 70
    confirmed_score: int = 80

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

