from __future__ import annotations

from typing import Any

from .adapter import JobAdapter
from .iloader import ILoader
from .iparser import IParser
from .template_compiler import TemplateCompiler


class JobBuilder:
    job: dict[str, Any]
    _adapter: JobAdapter | None
    _loader: ILoader | None
    _parser: IParser | None
    _template_compiler: TemplateCompiler | None

    def __init__(self) -> None:
        self.job = {}
        self._loader = None
        self._parser = None
        self._template_compiler = None
        self._adapter = None

    def loader(self, loader: ILoader) -> JobBuilder:
        self._loader = loader
        return self

    def parser(self, parser: IParser) -> JobBuilder:
        self._parser = parser
        return self

    def template_compiler(self, compiler: TemplateCompiler) -> JobBuilder:
        self._template_compiler = compiler
        return self

    def adapter(self, adapter: JobAdapter) -> JobBuilder:
        self._adapter = adapter
        return self

    def build(self) -> dict[str, Any]:
        assert self._loader is not None, "Loader is not provided"
        assert (
            self._template_compiler is not None
        ), "Template compiler is not provided"
        assert self._parser is not None, "Parser is not provided"
        assert self._adapter is not None, "Adapter is not provided"
        source_template = self._loader.load()
        compiled_template = self._template_compiler.compile(source_template)
        job = self._parser.parse(compiled_template)
        return self._adapter.adapt(job)
