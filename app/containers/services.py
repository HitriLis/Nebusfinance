from dependency_injector import containers, providers

from app.application.services.organization import OrganizationService


class ServicesContainer(containers.DeclarativeContainer):
    repository = providers.DependenciesContainer()

    organization_service = providers.Singleton(
        OrganizationService,
        repository=repository.organization_repository
    )

