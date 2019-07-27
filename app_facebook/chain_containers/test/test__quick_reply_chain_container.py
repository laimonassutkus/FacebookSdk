from app_facebook.chain_containers.quick_reply_chain_container import QuickReplyChainContainer
from app_facebook.chain_containers.test.test_case.chain_container_test_case import ChainContainerTestCase


class TestQuickReplyChainContainer(ChainContainerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = QuickReplyChainContainer()

    def test_get_chain(self):
        super().base_test_get_chain()
