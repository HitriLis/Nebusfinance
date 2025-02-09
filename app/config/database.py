from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    TEST_DB_NAME: str = "test_db"

    POOL_SIZE: int = 20
    ECHO_SQL: bool = False

    @property
    def db_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.DB_DRIVER,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME
        ).unicode_string()


db_settings = DatabaseSettings()
