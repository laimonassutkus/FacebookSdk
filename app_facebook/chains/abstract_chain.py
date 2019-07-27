from abc import ABC, abstractmethod
from app_facebook.events.abstract_event import AbstractEvent


class AbstractChain(ABC):
    def __init__(self, event: AbstractEvent, payload_uid: str):
        self.payload_uid = payload_uid
        self.event = event
        self.next_chain = None

    @abstractmethod
    def raise_event(self, payload: str, recipient_id: str) -> AbstractEvent:
        pass

    @abstractmethod
    def get_next_chain(self) -> 'AbstractChain':
        pass

    def set_next_chain(self, value: 'AbstractChain'):
        assert value, 'Next chain can not be empty.'

        self.next_chain = value
