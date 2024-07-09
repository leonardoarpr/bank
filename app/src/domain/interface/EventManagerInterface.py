from abc import ABC, abstractmethod

from app.src.domain.dto.event_dto import EventDTO


class EventManagerInterface(ABC):
    @abstractmethod
    def read_events(self) -> any:
        pass

    @abstractmethod
    def write_events(self) -> None:
        pass

    @abstractmethod
    def reset_events(self) -> None:
        pass

    @abstractmethod
    def find_event(self, destination) -> any:
        pass

    @abstractmethod
    def deposit(self, data: EventDTO) -> EventDTO:
        pass

    @abstractmethod
    def withdraw(self, data: EventDTO) -> EventDTO:
        pass

    @abstractmethod
    def transfer(self, data: EventDTO) -> (list, list):
        pass

    @abstractmethod
    def get_balance(self, account_id: str) -> int:
        pass
