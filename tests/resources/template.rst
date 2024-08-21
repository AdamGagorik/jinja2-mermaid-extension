{% mermaid -%}
ext: .png
name: test
mode: rst
diagram: |
    graph TD
        A --> B
        B --> C
        A --> C
{% endmermaid %}

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: rst
caption: |
    This is a test caption!
{% endmermaid %}

{% mermaid -%}
inp: test.mmd
ext: .png
name: test
mode: rst
just_name: true
{% endmermaid %}
