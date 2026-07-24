import os
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    BEDROCK_MODEL_ID: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode='after')
    def adjust_database_url(self) -> 'Settings':
     
        is_docker = os.path.exists('/.dockerenv') or os.environ.get('IS_DOCKER') == 'true'
        if is_docker and "localhost" in self.DATABASE_URL:
            self.DATABASE_URL = self.DATABASE_URL.replace("localhost", "ai-postgres")
        return self

settings = Settings()