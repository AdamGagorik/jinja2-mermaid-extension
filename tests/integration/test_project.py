from importlib.resources import files
from pathlib import Path

import pytest
from jinja2 import Environment, StrictUndefined

import tests.resources
from jinja2_mermaid_extension import MermaidExtension
from jinja2_mermaid_extension.base import runner
from jinja2_mermaid_extension.extension import TikZExtension


@pytest.fixture()
def run_root(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def resource_root() -> Path:
    return Path(str(files(tests.resources)))


@pytest.mark.parametrize(
    "template_name,expected_name,count",
    [
        pytest.param("template.md", "expected.md", 1, id="md"),
        pytest.param("template.rst", "expected.rst", 1, id="rst"),
        pytest.param("template.tikz.md", "expected.tikz.md", 3, id="md.tikz"),
    ],
)
def test_project(resource_root: Path, template_name: str, expected_name: str, run_root: Path, count: int):
    for path in run_root.iterdir():
        if path.suffix in {".png", ".svg"}:
            path.unlink()

    assert not any(run_root.iterdir())

    expected_path = resource_root / expected_name
    template_path = resource_root / template_name
    env = Environment(extensions=[MermaidExtension, TikZExtension], undefined=StrictUndefined)  # noqa: S701

    expected = env.from_string(expected_path.read_text()).render(tmp_path=run_root)
    rendered = env.from_string(template_path.read_text().replace("$tmp_path", str(run_root))).render(
        mermaid_input_root=resource_root,
        mermaid_output_root=run_root,
        tikz_input_root=resource_root,
        tikz_output_root=run_root,
    )

    runner().wait()
    assert rendered == expected
    assert len(list(run_root.iterdir())) == count
