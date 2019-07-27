from app_facebook.chains.none_chain import NoneChain
from app_facebook.chains.test.test_case.chain_dummy_test_case import ChainDummyTestCase
from app_facebook.events.none_event import NoneEvent


class TestNoneChain(ChainDummyTestCase):
    def test_raise_event(self):
        chain = NoneChain()

        # Raise event with a test payloads
        event = chain.raise_event('Test', 'recipient')

        # Expect that in any case a none event is returned
        self.assertIsInstance(event, NoneEvent)

    def test_get_next_chain(self):
        def expected_exception_func():
            # Try to get a next chain
            chain = NoneChain()
            chain.get_next_chain()

        # Assert that an exception was thrown
        with self.assertRaises(ValueError):
            expected_exception_func()

    def test_set_next_chain(self):
        def expected_exception_func():
            # Try to get a next chain
            chain = NoneChain()
            chain.set_next_chain(chain)

        # Assert that an exception was thrown
        with self.assertRaises(ValueError):
            expected_exception_func()
