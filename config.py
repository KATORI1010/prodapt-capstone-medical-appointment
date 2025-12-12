from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    PRODUCTION: bool
    DATABASE_URL: AnyUrl
    SUPABASE_URL: AnyUrl
    SUPABASE_KEY: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    RESEND_API_KEY: str
    OPENAI_API_KEY: str
    QDRANT_URL: AnyUrl
    QDRANT_API_KEY: str
    BRAINTRUST_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()