import json
import subprocess
from collections.abc import Iterable
from typing import Any

from jinja2_mermaid_extension.logger import logger


def run(command: Iterable[str], **kwargs: Any) -> None:
    """
    Run a command with subprocess and log the command.

    Args:
        command: The command to run.
        **kwargs: Extra arguments to pass to subprocess.run.
    """
    command = tuple(command)
    logger.debug(json.dumps(command, indent=2))
    subprocess.run(command, **kwargs)
