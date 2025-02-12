from dependency_injector import containers, providers

from app.containers.database import DatabaseContainer
from app.infrastructure.repositories.activity_repository import ActivityRepository
from app.infrastructure.repositories.organization_repository import OrganizationRepository


class RepositoryContainer(containers.DeclarativeContainer):

    database = providers.Container(DatabaseContainer)
    organization_repo = providers.Factory(
        OrganizationRepository,
        database.session
    )
    activity_repo = providers.Factory(
        ActivityRepository,
        database.session
    )
