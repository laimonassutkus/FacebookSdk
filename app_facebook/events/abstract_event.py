from abc import abstractmethod, ABC
from typing import List, Union
from app_facebook.payloads.payload import Payload
from app_facebook.view import View


class AbstractEvent(ABC):
    def __init__(self):
        self.__payload = None  # type: Payload
        self.__recipient = None  # type: str

    def payload(self) -> Payload:
        return self.__payload

    def recipient(self) -> str:
        return self.__recipient

    def inject_payload(self, payload: Payload):
        self.__payload = payload

    def inject_recipient(self, recipient: str):
        self.__recipient = recipient

    @abstractmethod
    def raise_view(self) -> Union[View, List[View]]:
        pass
