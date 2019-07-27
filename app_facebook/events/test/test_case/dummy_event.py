from app_facebook.events.abstract_event import AbstractEvent
from app_facebook.view import View


class DummyEvent(AbstractEvent):
    def __init__(self):
        super().__init__()

    def raise_view(self) -> View:
        return View(None)
