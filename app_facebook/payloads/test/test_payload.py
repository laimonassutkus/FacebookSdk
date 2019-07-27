from django.test import TestCase
from app_facebook.payloads.payload import Payload


class TestPayload(TestCase):
    def test_serialize(self):
        payload = Payload('TEST', { 'test': 'test' })

        # Serialize
        payload = payload.serialize()

        self.assertEqual(payload, '{"test": "test", "uid": "TEST"}')

    def test_deserialize(self):
        payload = Payload.deserialize('{"test": "test", "uid": "TEST"}')

        self.assertEqual(payload, Payload('TEST', { 'test': 'test' }))

    def test_match(self):
        self.assertTrue(Payload.match('{"test": "test", "uid": "TEST"}', 'TEST'))
