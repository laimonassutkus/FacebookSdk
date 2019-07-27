from app_facebook.chains.abstract_chain import AbstractChain
from app_facebook.chains.none_chain import NoneChain
from app_facebook.events.abstract_event import AbstractEvent
from app_facebook.payloads.payload import Payload


class Chain(AbstractChain):
    def __init__(self, event: AbstractEvent, payload_uid: str):
        super().__init__(event, payload_uid)

    def get_next_chain(self) -> 'AbstractChain':
        return self.next_chain or NoneChain()

    def raise_event(self, payload: str, recipient_id: str) -> AbstractEvent:
        if Payload.match(payload, self.payload_uid):
            self.event.inject_payload(Payload.deserialize(payload))
            self.event.inject_recipient(recipient_id)
            return self.event
        else:
            return self.get_next_chain().raise_event(payload, recipient_id)
