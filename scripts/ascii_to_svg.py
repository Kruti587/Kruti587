import html


def generate_svg(input_file, output_file):
    with open(input_file, "r") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]

    font_size = 11
    line_height = 15
    width = 900
    height = line_height * len(lines)

    svg_elements = []

    for i, line in enumerate(lines):
        escaped = html.escape(line)
        y = (i + 1) * line_height

        duration = 0.6 + len(line) * 0.01  # typing speed
        delay = i * 0.08

        svg_elements.append(
            f"""
<defs>
  <clipPath id="clip{i}">
    <rect x="0" y="{y - line_height + 3}" width="0" height="{line_height}">
      <animate attributeName="width"
               from="0" to="{width}"
               dur="{duration}s"
               begin="{delay}s"
               fill="freeze" />
    </rect>
  </clipPath>
</defs>

<text x="10" y="{y}"
      fill="#00ff88"
      font-family="Courier New, monospace"
      font-size="{font_size}"
      letter-spacing="1"
      xml:space="preserve"
      clip-path="url(#clip{i})">
  {escaped}
</text>

<!-- Cursor -->
<rect x="10" y="{y - line_height + 4}"
      width="8" height="{line_height - 4}"
      fill="#00ff88">
  <animate attributeName="x"
           from="10" to="{width}"
           dur="{duration}s"
           begin="{delay}s"
           fill="freeze" />
  <animate attributeName="opacity"
           values="1;0;1"
           dur="0.6s"
           repeatCount="indefinite" />
</rect>
"""
        )

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg"
 width="{width}" height="{height}"
 style="background:black">
{''.join(svg_elements)}
</svg>"""

    with open(output_file, "w") as f:
        f.write(svg_content)

    print(f"SVG saved to {output_file}")


if __name__ == "__main__":
    generate_svg("assets/ascii.txt", "assets/portrait.svg")
