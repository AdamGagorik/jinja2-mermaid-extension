# Path Output + Raw Input

./test.png

# Path Output + Markdown Input

./test.png

# Markdown Output + Markdown Input

![test.png](./test.png)

# Markdown Output (just_name) + Markdown Input

![test.png](test.png)

# Markdown Output (full_path) + Markdown Input

![test.png]({{ tmp_path / 'test.png' }})

# MyST Output (just_name) + Markdown Input

:::{image} test.png
:align: center
:::

# MyST Output + Markdown Input + Caption

:::{figure} ./test.png
:align: center

This is a test caption!
:::
