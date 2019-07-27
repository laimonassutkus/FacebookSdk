from app_facebook.chain_containers.abstract_chain_container import AbstractChainContainer


class MessagesChainContainer(AbstractChainContainer):
    __instance = None

    def __new__(cls):
        if not MessagesChainContainer.__instance:
            MessagesChainContainer.__instance = object.__new__(cls)

            cls.chains = []

        return MessagesChainContainer.__instance
