from jinja2 import Environment

from jinja2_mermaid_extension.extension import MermaidExtension


def test_register_extension():
    Environment(extensions=[MermaidExtension])  # noqa: S701
