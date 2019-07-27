from abc import ABC, abstractmethod


class BaseMessageObject(ABC):
    @abstractmethod
    def to_json(self):
        pass
