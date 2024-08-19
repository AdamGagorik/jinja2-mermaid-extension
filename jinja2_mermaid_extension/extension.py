import inspect
from collections.abc import Generator
from pathlib import Path
from typing import Any

from jinja2 import Environment

from jinja2_mermaid_extension.base import GenImageExtension
from jinja2_mermaid_extension.callback import mermaid


class MermaidExtension(GenImageExtension):
    tags: set[str] = {"mermaid"}  # noqa: RUF012

    def __init__(self, environment: Environment):
        super().__init__(environment)

    @property
    def _valid_keys(self) -> Generator[str]:
        yield from inspect.signature(mermaid).parameters

    @staticmethod
    def modify(**kwargs: Any) -> Generator[tuple[str, Any], None, None]:
        for key, value in kwargs.items():
            if key == "diagram":
                if "inp" in kwargs:
                    raise RuntimeError("Cannot have both 'diagram' and 'inp' in kwargs")
                yield "inp", value
            else:
                yield key, value

    def callback(
        self,
        inp: Path | str,
        out: Path,
        **kwargs: Any,
    ) -> None:
        if isinstance(inp, str) and inp.endswith(".mmd"):
            inp = Path(inp)

        return mermaid(inp=inp, out=out, **kwargs)
