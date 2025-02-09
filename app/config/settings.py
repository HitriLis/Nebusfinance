from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str


settings = Settings()
