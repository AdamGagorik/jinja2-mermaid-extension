# Path Output + Raw Input

{% tikz -%}
ext: .pdf
name: test
mode: path
diagram: |
    \documentclass[margin=0pt]{standalone}
    \usepackage{tikz}
    \begin{document}
    \begin{tikzpicture}[remember picture]
    \coordinate (SE) at (0,0) {};
    \coordinate (NW) at (5,5) {};
    \draw (SE) rectangle (NW);
    \node[draw, rectangle, anchor=south west] at (SE) {SE};
    \node[draw, rectangle, anchor=north east] at (NW) {NW};
    \end{tikzpicture}
    \end{document}
{% endtikz %}

# Path Output + Markdown Input

{% tikz -%}
inp: test.tex
ext: .pdf
name: test
mode: path
{% endtikz %}

# Path Output + Markdown Input + SVG

{% tikz -%}
inp: test.tex
ext: .svg
name: test
mode: path
{% endtikz %}

# Path Output + Markdown Input + PNG

{% tikz -%}
inp: test.tex
ext: .png
name: test
mode: path
{% endtikz %}

# Raw Input + Missing documentclass

{% tikz -%}
ext: .pdf
name: test2
mode: path
diagram: |
    \node[draw, fill=yellow] at (0,0) {\textcolor{blue}{Hello, world!}};
{% endtikz %}
