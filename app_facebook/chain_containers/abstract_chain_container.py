from abc import ABC
from typing import List
from app_facebook.chains.abstract_chain import AbstractChain
from app_facebook.chains.chain import Chain
from app_facebook.chains.none_chain import NoneChain


class AbstractChainContainer(ABC):
    def __init__(self):
        self.chains = []  # type: List[Chain]

    def __repr__(self):
        chain_names = [chain.__class__.__name__ for chain in self.chains]

        return 'Total chains: {}\nChains:\n{}'.format(
            len(self.chains),
            '\n'.join(chain_names)
        )

    def get_chain(self) -> AbstractChain:
        if not len(self.chains):
            return NoneChain()

        chain = current_chain = self.chains[0]

        for chain_index in range(0, len(self.chains) - 1):
            current_chain.set_next_chain(self.chains[chain_index + 1])
            current_chain = current_chain.get_next_chain()

        return chain
