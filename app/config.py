import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Enterprise AI CRM"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./crm.db")
    AI_CONFIDENCE_THRESHOLD: float = 0.65

settings = Settings()
