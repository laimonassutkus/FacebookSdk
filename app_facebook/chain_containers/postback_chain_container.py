from app_facebook.chain_containers.abstract_chain_container import AbstractChainContainer


class PostbackChainContainer(AbstractChainContainer):
    __instance = None

    def __new__(cls):
        if not PostbackChainContainer.__instance:
            PostbackChainContainer.__instance = object.__new__(cls)

            cls.chains = []

        return PostbackChainContainer.__instance
