from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    PRODUCTION: bool
    DATABASE_URL: AnyUrl
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    OPENAI_API_KEY: str
    WORKFLOW_ID: str
    BRAINTRUST_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
