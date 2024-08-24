from importlib.resources import files
from pathlib import Path

import pytest
from jinja2 import Environment, StrictUndefined

import tests.resources
from jinja2_mermaid_extension import MermaidExtension
from jinja2_mermaid_extension.base import runner


@pytest.fixture()
def run_root(tmp_path: Path) -> Path:
    return tmp_path


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
def test_project(resource_root: Path, template_name: str, expected_name: str, run_root: Path):
    for path in run_root.iterdir():
        if path.suffix in {".png", ".svg"}:
            path.unlink()

    assert not any(run_root.iterdir())

    expected_path = resource_root / expected_name
    template_path = resource_root / template_name
    env = Environment(extensions=[MermaidExtension], undefined=StrictUndefined)  # noqa: S701

    expected = env.from_string(expected_path.read_text()).render(tmp_path=run_root)
    rendered = env.from_string(template_path.read_text().replace("$tmp_path", str(run_root))).render(
        mermaid_input_root=resource_root,
        mermaid_output_root=run_root,
    )

    runner().wait()
    assert rendered == expected
    assert len(list(run_root.iterdir())) == 1
