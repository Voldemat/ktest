from abc import ABC, abstractmethod
from typing import Any

PARSER_RETURN_TYPE = dict[str, Any]


class IParser(ABC):
    @abstractmethod
    def parse(self, value: str) -> PARSER_RETURN_TYPE:
        pass
