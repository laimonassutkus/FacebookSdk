from app_facebook.events.test.test_case.event_dummy_test_case import EventDummyTestCase
from app_facebook.payloads.payload import Payload


class TestAbstractEvent(EventDummyTestCase):
    def test_inject_payload(self):
        event = self.dummy_event()
        payload = Payload('Test')

        event.inject_payload(payload)

        self.assertEqual(event.payload(), payload)

    def test_payload(self):
        event = self.dummy_event()
        payload = Payload('Test')

        event.inject_payload(payload)

        self.assertEqual(event.payload(), payload)

    def test_inject_recipient(self):
        event = self.dummy_event()
        event.inject_recipient('test')

        self.assertEqual(event.recipient(), 'test')

    def test_recipient(self):
        event = self.dummy_event()
        event.inject_recipient('test')

        self.assertEqual(event.recipient(), 'test')
