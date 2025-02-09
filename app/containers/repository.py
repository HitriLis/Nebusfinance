from dependency_injector import containers, providers

from app.containers.database import DatabaseContainer
from app.infrastructure.repositories.organization_repository import OrganizationRepository


class RepositoryContainer(containers.DeclarativeContainer):
    # config = providers.Configuration()

    database = providers.Container(DatabaseContainer)
    organization_repository = providers.Factory(
        OrganizationRepository,
        database.session
    )
    # qr_code_repository = providers.Factory(
    #     SQLAlchemyQRCodeRepository,
    #     database.session
    # )
