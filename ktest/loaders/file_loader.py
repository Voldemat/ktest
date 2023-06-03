from ..iloader import ILoader


class FileLoader(ILoader):
    def __init__(self, path: str) -> None:
        self.path = path

    def load(self) -> str:
        with open(self.path, "r") as file:
            return file.read()
