import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Todo Backend with Authentication"
    version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_HGztRF0Pgx3l@ep-small-brook-adtw8asl-pooler.c-2.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require")
    
    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days
    
    # Rate limiting
    auth_attempts_per_minute: int = int(os.getenv("AUTH_ATTEMPTS_PER_MINUTE", "5"))
    
    # Other settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"


settings = Settings()