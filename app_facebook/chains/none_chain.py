import logging

from app_facebook.chains.abstract_chain import AbstractChain
from app_facebook.events.abstract_event import AbstractEvent
from app_facebook.events.none_event import NoneEvent

logr = logging.getLogger(__name__)


class NoneChain(AbstractChain):
    def __init__(self):
        super().__init__(NoneEvent(), 'NONE_PAYLOAD')

    def raise_event(self, payload: str, recipient_id: str) -> AbstractEvent:
        return self.event

    def get_next_chain(self) -> AbstractChain:
        raise ValueError('This method should never be called.')

    def set_next_chain(self, value: AbstractChain):
        raise ValueError('This method should never be called.')
