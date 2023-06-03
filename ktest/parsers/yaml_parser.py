import yaml

from ..iparser import IParser, PARSER_RETURN_TYPE


class YamlParser(IParser):
    def parse(self, value: str) -> PARSER_RETURN_TYPE:
        return yaml.safe_load(value)  # type: ignore [no-any-return]
