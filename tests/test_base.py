from jinja2 import Environment

from jinja2_mermaid_extension.base import GenImageExtension


def test_register_extension():
    Environment(extensions=[GenImageExtension])  # noqa: S701
