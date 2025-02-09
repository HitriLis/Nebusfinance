from dependency_injector import containers, providers

from app.containers.repository import RepositoryContainer
from app.containers.services import ServicesContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repository = providers.Container(
        RepositoryContainer
    )

    services = providers.Container(
        ServicesContainer,
        repository=repository
    )






