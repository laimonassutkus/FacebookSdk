from django.test import TestCase
from app_facebook.events.test.test_case.dummy_event import DummyEvent


class EventDummyTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dummy_event(self):
        return DummyEvent()
