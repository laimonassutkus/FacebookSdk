from django.test import TestCase
from app_facebook.chains.chain import Chain
from app_facebook.events.test.test_case.event_dummy_test_case import EventDummyTestCase


class ChainDummyTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_dummy_test_case = EventDummyTestCase()

    def dummy_chain(self):
        return Chain(self.event_dummy_test_case.dummy_event(), 'TEST')
