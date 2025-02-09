from dependency_injector import containers, providers


class ServicesContainer(containers.DeclarativeContainer):
    repository = providers.DependenciesContainer()

