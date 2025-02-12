from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str


settings = Settings()
