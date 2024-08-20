import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from jinja2_mermaid_extension.callback import mermaid


@pytest.mark.parametrize(
    "inp,theme,scale,width,height,background",
    [
        pytest.param("raw", "default", 3, 800, None, "white", id="default"),
    ],
)
def test_mermaid(
    inp: Path | str,
    theme: str,
    scale: int,
    width: int,
    height: int | None,
    background: str,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
):
    out = tmp_path / "out" / "test.png"
    out.parent.mkdir(parents=True, exist_ok=False)

    def side_effect(command: list[str]) -> None:
        assert f"-s {scale}" in " ".join(command)
        (tmp_path / "test.png").write_text("test")

    with monkeypatch.context() as m:
        mock_check_call = Mock(spec=subprocess.check_call, side_effect=side_effect)
        m.setattr(subprocess, "check_call", lambda *args, **kwargs: mock_check_call(*args, **kwargs))
        mermaid(inp, out, theme, scale, width, height, background, temp_dir=tmp_path)
        mock_check_call.assert_called_once()
