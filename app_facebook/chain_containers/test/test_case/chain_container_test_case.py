from django.test import TestCase
from app_facebook.chain_containers.abstract_chain_container import AbstractChainContainer
from app_facebook.chains.test.test_case.chain_dummy_test_case import ChainDummyTestCase


class ChainContainerTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = None  # type: AbstractChainContainer
        self.chain_dummy_test_case = ChainDummyTestCase()

    def base_test_get_chain(self):
        chain1 = self.chain_dummy_test_case.dummy_chain()
        chain2 = self.chain_dummy_test_case.dummy_chain()

        # Add chains to the container
        self.container.chains = [chain1, chain2]

        # Create single chain
        chain = self.container.get_chain()

        # Assert first chain
        self.assertEqual(chain, chain1)
        # Assert second chain
        self.assertEqual(chain.get_next_chain(), chain2)
