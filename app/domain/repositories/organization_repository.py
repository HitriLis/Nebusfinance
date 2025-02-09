from abc import ABC, abstractmethod
from typing import List
from ..entities.organization import Organization


class IOrganizationRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Organization]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, organization_id: int) -> Organization:
        raise NotImplementedError

    @abstractmethod
    def get_by_activity(self, activity_id: int) -> List[Organization]:
        raise NotImplementedError
