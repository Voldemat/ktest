from __future__ import annotations


class TemplateCompiler:
    values: dict[str, str]

    def __init__(self) -> None:
        self.values = {}

    @staticmethod
    def build_template_name(name: str) -> str:
        return f"<{name}>"

    def set(self, name: str, value: str) -> TemplateCompiler:
        self.values[name] = value
        return self

    def set_many(self, values: dict[str, str]) -> TemplateCompiler:
        self.values = {**self.values, **values}
        return self

    def compile(self, template: str) -> str:
        for name, value in self.values.items():
            template = template.replace(self.build_template_name(name), value)
        return template
