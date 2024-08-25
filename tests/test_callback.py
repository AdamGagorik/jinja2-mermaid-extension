import subprocess
from collections.abc import Hashable
from pathlib import Path
from typing import Any, Callable
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
        mermaid(
            inp=inp,
            out=out,
            theme=theme,
            scale=scale,
            render_width=width,
            render_height=height,
            background=background,
            temp_dir=tmp_path,
        )
        mock_check_call.assert_called_once()


def touch(tmp_path: Path, *names: str) -> Path:
    path = tmp_path.joinpath(*names)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


@pytest.mark.parametrize(
    "callback_kwargs,setup_effect,exception,phrase,expect_called",
    [
        pytest.param(
            {
                "inp": Path("missing.mmd"),
                "out": Path("output.png"),
            },
            lambda tmp_path: None,
            FileNotFoundError,
            "input file does not exist!",
            False,
            id="FileNotFoundError(inp)",
        ),
        pytest.param(
            {
                "inp": "raw",
                "out": lambda tmp_path: tmp_path / "a" / "b.png",
            },
            lambda tmp_path: None,
            FileNotFoundError,
            "output directory does not exist!",
            False,
            id="FileNotFoundError(out)",
        ),
        pytest.param(
            {
                "inp": "raw",
                "out": lambda tmp_path: tmp_path,
            },
            lambda tmp_path: None,
            IsADirectoryError,
            lambda tmp_path: str(tmp_path),
            False,
            id="IsADirectoryError",
        ),
        pytest.param(
            {
                "inp": "raw",
                "out": Path("exists.png"),
            },
            lambda tmp_path: touch(tmp_path, "exists.png"),
            FileExistsError,
            lambda tmp_path: str(tmp_path),
            False,
            id="FileExistsError",
        ),
        pytest.param(
            {
                "inp": "raw",
                "out": "wrong.txt",
            },
            lambda tmp_path: None,
            ValueError,
            "Expected output file to have a .* extension",
            False,
            id="ValueError(out)",
        ),
        pytest.param(
            {
                "inp": lambda tmp_path: touch(tmp_path, "inp", "wrong.pdf"),
                "out": "right.png",
            },
            lambda tmp_path: tmp_path.joinpath("wrong.pdf").touch(),
            ValueError,
            "Expected input file to have a .mmd extension",
            False,
            id="ValueError(inp)",
        ),
        pytest.param(
            {
                "inp": lambda tmp_path: touch(tmp_path, "inp", "input.mmd"),
                "out": "output.png",
            },
            lambda tmp_path: tmp_path.joinpath("wrong.pdf").touch(),
            RuntimeError,
            "Failed to execute command",
            True,
            id="RuntimeError",
        ),
    ],
)
def test_mermaid_raises(
    callback_kwargs: dict[Hashable, Any],
    setup_effect: Callable[[Path], None],
    exception: type[Exception],
    phrase: str | Callable[[Path], str],
    expect_called: bool,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
):
    setup_effect(tmp_path)

    if callable(phrase):
        phrase = phrase(tmp_path)

    for key, value in callback_kwargs.items():
        if callable(value):
            callback_kwargs[key] = value(tmp_path)

    def side_effect(command: list[str]) -> None:
        raise subprocess.CalledProcessError(1, command)

    with monkeypatch.context() as m:
        mock_check_call = Mock(spec=subprocess.check_call, side_effect=side_effect)
        m.setattr(subprocess, "check_call", lambda *args, **kwargs: mock_check_call(*args, **kwargs))
        with pytest.raises(exception, match=phrase):
            mermaid(**callback_kwargs, temp_dir=tmp_path)

        if not expect_called:
            mock_check_call.assert_not_called()
