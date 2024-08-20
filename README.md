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

The following arguments are available:

| Argument                 | Description                                                                | Default                |
| ------------------------ | -------------------------------------------------------------------------- | ---------------------- |
| **diagram**              | The diagram to render.                                                     | `None`                 |
| **ext**                  | The file extension of the generated diagram.                               | `".png"`               |
| **theme**                | The theme to use for the diagram.                                          | `"default"`            |
| **scale**                | A scaling factor for the diagram.                                          | `3`                    |
| **width**                | The width of the diagram in pixels.                                        | `800 `                 |
| **height**               | The height of the diagram in pixels.                                       | `None`                 |
| **background**           | The background color of the generated diagram.                             | `"white"`              |
| **align**                | The alignment of the diagram in the rendered string.                       | `"center"`             |
| **caption**              | A caption to add to the diagram.                                           | `None`                 |
| **use_cached**           | Whether to use a cached version of the diagram.                            | `True`                 |
| **use_myst_syntax**      | Whether to use the `myst` syntax for the diagram.                          | `True`                 |
| **temp_dir**             | A temporary directory to use for intermediate files.                       | `None`                 |
| **delete_temp_dir**      | Whether to delete the temporary directory after execution.                 | `True`                 |
| **mermaid_docker_image** | The docker image containing the mermaid-cli tool.                          | `"minlag/mermaid-cli"` |
| **mermaid_volume_mount** | The directory in the docker container to mount the temporary directory to. | `"/data"`              |

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
