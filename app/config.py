from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    env: str = os.getenv("ENV", "development")
    debug: bool = os.getenv("DEBUG", True)
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./budget_buddy.db")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
