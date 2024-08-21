from importlib.resources import files
from pathlib import Path

import pytest
from jinja2 import Environment, StrictUndefined

import tests.resources
from jinja2_mermaid_extension import MermaidExtension


@pytest.fixture()
def resource_root() -> Path:
    return Path(str(files(tests.resources)))


@pytest.mark.parametrize(
    "template_name,expected_name",
    [
        pytest.param("template.md", "expected.md", id="md"),
        pytest.param("template.rst", "expected.rst", id="rst"),
    ],
)
def test_project(resource_root: Path, template_name: str, expected_name: str, tmp_path: Path):
    assert not any(tmp_path.iterdir())
    template_path = resource_root / template_name
    expected_path = resource_root / expected_name
    env = Environment(extensions=[MermaidExtension], undefined=StrictUndefined)  # noqa: S701
    expected = env.from_string(expected_path.read_text()).render(tmp_path=tmp_path)
    rendered = env.from_string(template_path.read_text().replace("$tmp_path", str(tmp_path))).render(
        mermaid_output_root=tmp_path
    )
    assert len(list(tmp_path.iterdir())) == 1
    assert rendered == expected
