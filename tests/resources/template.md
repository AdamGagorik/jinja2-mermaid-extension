# Path Output + Raw Input

{% mermaid -%}
ext: .png
name: test
mode: path
diagram: |
    graph TD
        A --> B
        B --> C
        A --> C
{% endmermaid %}

# Path Output + Markdown Input

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: path
{% endmermaid %}

# Markdown Output + Markdown Input

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: markdown
{% endmermaid %}

# Markdown Output (just_name) + Markdown Input

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: markdown
just_name: true
{% endmermaid %}

# Markdown Output (relative_to) + Markdown Input

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: markdown
relative_to: $tmp_path
{% endmermaid %}

# MyST Output (just_name) + Markdown Input

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: myst
just_name: true
{% endmermaid %}

# MyST Output + Markdown Input + Caption

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: myst
caption: |
    This is a test caption!
{% endmermaid %}
