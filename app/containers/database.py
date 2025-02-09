from dependency_injector import containers, providers
from app.config.database import db_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async def async_session_generator(session_factory):
    async with session_factory() as session:
        yield session


class DatabaseContainer(containers.DeclarativeContainer):
    engine = providers.Singleton(
        create_async_engine,
        url=db_settings.db_url,
        pool_size=db_settings.POOL_SIZE,
        echo=db_settings.ECHO_SQL
    )
    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine
    )

    session = providers.Resource(
        async_session_generator,
        session_factory=session_factory,
    )
