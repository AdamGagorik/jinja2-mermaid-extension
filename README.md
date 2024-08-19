# jinja2-mermaid-extension

[![Release](https://img.shields.io/github/v/release/AdamGagorik/jinja2-mermaid-extension)](https://img.shields.io/github/v/release/AdamGagorik/jinja2-mermaid-extension)
[![Build status](https://img.shields.io/github/actions/workflow/status/AdamGagorik/jinja2-mermaid-extension/main.yml?branch=main)](https://github.com/AdamGagorik/jinja2-mermaid-extension/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/AdamGagorik/jinja2-mermaid-extension/branch/main/graph/badge.svg)](https://codecov.io/gh/AdamGagorik/jinja2-mermaid-extension)
[![Commit activity](https://img.shields.io/github/commit-activity/m/AdamGagorik/jinja2-mermaid-extension)](https://img.shields.io/github/commit-activity/m/AdamGagorik/jinja2-mermaid-extension)
[![License](https://img.shields.io/github/license/AdamGagorik/jinja2-mermaid-extension)](https://img.shields.io/github/license/AdamGagorik/jinja2-mermaid-extension)

A jinja2 block to render a mermaid diagram.

- **Github repository**: <https://github.com/AdamGagorik/jinja2-mermaid-extension/>
- **Documentation** <https://AdamGagorik.github.io/jinja2-mermaid-extension/>

## Setup

- `Docker` must be installed to run the `mermaid` command line tool.
- The extension should be installed in your `Python` environment.

```bash
pip install jinja2-mermaid-extension
```

- The extension should be added to the `jinja2` environment.

```python
from jinja2 import Environment
from jinja2_mermaid_extension import MermaidExtension

env = Environment(extensions=[MermaidExtension])
```

## Usage

The following `jinaj2` block will be transformed into an image and referenced in the rendered string.

```jinja2
{% mermaid -%}
theme: default
scale: 3
width: 75
align: center
caption: |
    An example mermaid diagram!
diagram: |
    graph TD
        A --> B
        B --> C
        A --> C
{% endmermaid %}
```

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
