from app_facebook.chains.chain import Chain
from app_facebook.chains.none_chain import NoneChain
from app_facebook.chains.test.test_case.chain_dummy_test_case import ChainDummyTestCase
from app_facebook.events.none_event import NoneEvent
from app_facebook.payloads.payload import Payload
from app_facebook.test.test_case.base_test_case import BaseTestCase


class TestChain(ChainDummyTestCase):
    @BaseTestCase.generate(('PAYLOAD1', 'PAYLOAD1'), ('PAYLOAD1', 'PAYLOAD2'))
    def test_raise_event(self, chain_payload_uid: str, payload_uid: str):
        event = self.event_dummy_test_case.dummy_event()

        # Create a chain that accepts payloads with a specified payloads uid
        chain = Chain(event, chain_payload_uid)
        payload = Payload(payload_uid)

        # Raise event with a serialized payloads
        matched_event = chain.raise_event(payload.serialize(), 'recipient')

        # If payloads match - events must be the same
        # If they don't - event must not match
        if chain_payload_uid == payload_uid:
            # Assert that matched event is the same
            self.assertEqual(matched_event, event)
        else:
            # Asset that event is a none event
            self.assertIsInstance(matched_event, NoneEvent)

    @BaseTestCase.generate(True, False)
    def test_get_next_chain(self, next_chain_exists: bool):
        event = self.event_dummy_test_case.dummy_event()

        chain1 = Chain(event, 'Test1')
        chain2 = Chain(event, 'Test2')

        if next_chain_exists:
            chain1.next_chain = chain2

        if next_chain_exists:
            # Assert that next chain is the second chain
            self.assertEqual(chain1.get_next_chain(), chain2)
        else:
            self.assertIsInstance(chain1.get_next_chain(), NoneChain)

    def test_set_next_chain(self):
        event = self.event_dummy_test_case.dummy_event()

        chain1 = Chain(event, 'Test1')
        chain2 = Chain(event, 'Test2')

        # Make sure chain is none
        self.assertIsNone(chain1.next_chain)

        # Set next chain
        chain1.set_next_chain(chain2)

        # Make sure next chain was set
        self.assertEqual(chain1.next_chain, chain2)
