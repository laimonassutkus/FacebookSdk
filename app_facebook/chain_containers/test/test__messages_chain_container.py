from app_facebook.chain_containers.messages_chain_container import MessagesChainContainer
from app_facebook.chain_containers.test.test_case.chain_container_test_case import ChainContainerTestCase


class TestMessagesChainContainer(ChainContainerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = MessagesChainContainer()

    def test_get_chain(self):
        super().base_test_get_chain()