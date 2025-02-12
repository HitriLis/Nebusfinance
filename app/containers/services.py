from dependency_injector import containers, providers

from app.application.services.organization import OrganizationService


class ServicesContainer(containers.DeclarativeContainer):
    repository = providers.DependenciesContainer()

    organization_service = providers.Singleton(
        OrganizationService,
        organizations_repo=repository.organization_repo,
        activity_repo=repository.activity_repo
    )

