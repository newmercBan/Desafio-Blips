from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lead Management API"
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "leads_db"
    EXTERNAL_API_URL: str = "https://dummyjson.com/users/1"

    class Config:
        env_file = ".env"

settings = Settings()
