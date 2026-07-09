from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "F5 Management Platform"
    APP_VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/f5_platform"
    CLICKHOUSE_URL: str = "http://localhost:8123"
    CLICKHOUSE_DATABASE: str = "f5_platform"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()