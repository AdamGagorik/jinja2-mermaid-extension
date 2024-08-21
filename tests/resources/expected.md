# Path Output + Raw Input

{{ tmp_path / 'test.png' }}

# Path Output + Markdown Input

{{ tmp_path / 'test.png' }}

# Markdown Output + Markdown Input

![test.png]({{ tmp_path / 'test.png' }})

# Markdown Output (just_name) + Markdown Input

![test.png](test.png)

# Markdown Output (relative_to) + Markdown Input

![test.png](test.png)

# MyST Output (just_name) + Markdown Input

:::{image} test.png
:align: center
:::

# MyST Output + Markdown Input + Caption

:::{figure} {{ tmp_path / 'test.png' }}
:align: center

This is a test caption!
:::
