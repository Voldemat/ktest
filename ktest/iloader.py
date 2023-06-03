from abc import ABC, abstractmethod


class ILoader(ABC):
    @abstractmethod
    def load(self) -> str:
        pass
