import inspect
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
from jinja2 import Environment
from pytest import MonkeyPatch

import jinja2_mermaid_extension.extension
from jinja2_mermaid_extension.base import Mode
from jinja2_mermaid_extension.extension import MermaidExtension


def test_register_extension():
    Environment(extensions=[MermaidExtension])  # noqa: S701


TEST_TEMPLATE = r"""
{{% mermaid -%}}
ext: .png
name: test
mode: {mode}
scale: 3
width: 75
align: center
caption: |
    An example mermaid diagram!
diagram: |
    graph TD
        A --> B
        B --> C
        A --> C
{{% endmermaid %}}
"""


@pytest.mark.parametrize(
    "mode",
    [
        pytest.param(Mode.OUT, id="OUT"),
    ],
)
def test_run_extension(mode: Mode, monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    def side_effect(inp: Path | str, out: Path, **kwargs: Any) -> None:
        pass

    mock_mermaid = Mock(spec=jinja2_mermaid_extension.extension.mermaid, side_effect=side_effect)
    mock_mermaid.__signature__ = inspect.signature(jinja2_mermaid_extension.extension.mermaid)

    with monkeypatch.context() as m:
        m.setattr(jinja2_mermaid_extension.extension, "mermaid", mock_mermaid)
        env = Environment(extensions=[MermaidExtension])  # noqa: S701
        template = env.from_string(TEST_TEMPLATE.format(mode=mode.value))
        rendered = template.render(mermaid_output_root=tmp_path).strip()
        assert rendered == str(tmp_path.joinpath("test.png"))
        mock_mermaid.assert_called_once()
