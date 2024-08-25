import subprocess
from collections.abc import Hashable
from pathlib import Path
from typing import Any, Callable
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from jinja2_mermaid_extension.callback import mermaid, tikz


@pytest.mark.parametrize(
    "callback_kwargs,call_contains",
    [
        pytest.param(
            lambda p: {
                "inp": "raw",
            },
            ("tectonic", "test.tex"),
            id="default",
        ),
    ],
)
def test_tikz(
    callback_kwargs: Callable[[Path], dict[Hashable, Any]],
    call_contains: tuple[str, ...],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
):
    do_run_callback_test(tikz, callback_kwargs, call_contains, "pdf", tmp_path, monkeypatch)


def do_run_callback_test(
    callback: Callable[..., None],
    callback_kwargs: Callable[[Path], dict[Hashable, Any]],
    call_contains: tuple[str, ...],
    out_ext: str,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
):
    callback_kwargs = callback_kwargs(tmp_path)
    out = tmp_path / "out" / f"test.{out_ext}"
    out.parent.mkdir(parents=True, exist_ok=False)

    def side_effect(command: list[str]) -> None:
        (tmp_path / f"test.{out_ext}").write_text("test")
        assert command

    with monkeypatch.context() as m:
        mock_check_call = Mock(spec=subprocess.check_call, side_effect=side_effect)
        m.setattr(subprocess, "check_call", lambda *args, **kwargs: mock_check_call(*args, **kwargs))
        callback(**callback_kwargs, out=out, temp_dir=tmp_path)

        assert out.exists()
        mock_check_call.assert_called_once()
        for arg in call_contains:
            assert arg in mock_check_call.call_args.args[0]


@pytest.mark.parametrize(
    "callback_kwargs,call_contains",
    [
        pytest.param(
            lambda p: {
                "inp": "raw",
            },
            ("docker",),
            id="default",
        ),
        pytest.param(
            lambda p: {
                "inp": "raw",
                "use_local_mmdc_instead": True,
            },
            ("mmdc",),
            id="local",
        ),
    ],
)
def test_mermaid(
    callback_kwargs: Callable[[Path], dict[Hashable, Any]],
    call_contains: tuple[str, ...],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
):
    do_run_callback_test(mermaid, callback_kwargs, call_contains, "png", tmp_path, monkeypatch)


def touch(root: Path, *names: str) -> Path:
    path = root.joinpath(*names)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


@pytest.mark.parametrize(
    "callback",
    [
        pytest.param(tikz, id="tikz"),
        pytest.param(mermaid, id="mermaid"),
    ],
)
@pytest.mark.parametrize(
    "callback_kwargs,setup_effect,exception,phrase,expect_called",
    [
        pytest.param(
            lambda p: {
                "inp": Path("missing.mmd"),
                "out": Path("output.png"),
            },
            lambda p: None,
            FileNotFoundError,
            "input file does not exist!",
            False,
            id="FileNotFoundError(inp)",
        ),
        pytest.param(
            lambda p: {
                "inp": "raw",
                "out": p / "a" / "b.png",
            },
            lambda p: None,
            FileNotFoundError,
            "output directory does not exist!",
            False,
            id="FileNotFoundError(out)",
        ),
        pytest.param(
            lambda p: {
                "inp": "raw",
                "out": p,
            },
            lambda p: None,
            IsADirectoryError,
            lambda p: str(p),
            False,
            id="IsADirectoryError",
        ),
        pytest.param(
            lambda p: {
                "inp": "raw",
                "out": Path("exists.png"),
            },
            lambda p: touch(p, "exists.png"),
            FileExistsError,
            lambda p: str(p),
            False,
            id="FileExistsError",
        ),
        pytest.param(
            lambda p: {
                "inp": "raw",
                "out": "wrong.txt",
            },
            lambda p: None,
            ValueError,
            "Expected output file to have a .* extension",
            False,
            id="ValueError(out)",
        ),
        pytest.param(
            lambda p: {
                "inp": touch(p, "inp", "wrong.pdf"),
                "out": "right.pdf",
            },
            lambda p: p.joinpath("wrong.pdf").touch(),
            ValueError,
            "Expected input file to have a .* extension.*",
            False,
            id="ValueError(inp)",
        ),
        pytest.param(
            lambda p: {
                "inp": "raw",
                "out": "output.pdf",
            },
            lambda p: p.joinpath("wrong.pdf").touch(),
            RuntimeError,
            "Failed to execute command",
            True,
            id="RuntimeError",
        ),
    ],
)
def test_callback_raises(
    callback: Callable[..., None],
    callback_kwargs: Callable[[Path], dict[Hashable, Any]],
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

    callback_kwargs = callback_kwargs(tmp_path)

    def side_effect(command: list[str]) -> None:
        raise subprocess.CalledProcessError(1, command)

    with monkeypatch.context() as m:
        mock_check_call = Mock(spec=subprocess.check_call, side_effect=side_effect)
        m.setattr(subprocess, "check_call", lambda *args, **kwargs: mock_check_call(*args, **kwargs))
        with pytest.raises(exception, match=phrase):
            callback(**callback_kwargs, temp_dir=tmp_path)

        if not expect_called:
            mock_check_call.assert_not_called()
