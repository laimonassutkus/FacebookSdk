from app_facebook.chain_containers.postback_chain_container import PostbackChainContainer
from app_facebook.chain_containers.test.test_case.chain_container_test_case import ChainContainerTestCase


class TestPostbackChainContainer(ChainContainerTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = PostbackChainContainer()

    def test_get_chain(self):
        super().base_test_get_chain()
