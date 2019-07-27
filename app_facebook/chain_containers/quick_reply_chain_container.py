from app_facebook.chain_containers.abstract_chain_container import AbstractChainContainer


class QuickReplyChainContainer(AbstractChainContainer):
    __instance = None

    def __new__(cls):
        if not QuickReplyChainContainer.__instance:
            QuickReplyChainContainer.__instance = object.__new__(cls)

            cls.chains = []

        return QuickReplyChainContainer.__instance
