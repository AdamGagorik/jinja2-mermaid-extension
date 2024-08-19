import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from jinja2_mermaid_extension.callback import mermaid


@pytest.mark.parametrize("inp,out,theme,scale,width,height,background_color", [])
def test_mermaid(
    inp: Path | str,
    out: Path,
    theme: str,
    scale: int,
    width: int,
    height: int,
    background_color: str,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
):
    inp = tmp_path / inp
    out = tmp_path / out
    with monkeypatch.context() as m:
        mock_run = MagicMock()
        m.setattr(subprocess, "run", lambda *args, **kwargs: mock_run(*args, **kwargs))
        mermaid(inp, out, theme, scale, width, height, background_color)
        mock_run.assert_called_once()
