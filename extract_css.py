#!/usr/bin/env python3
"""
Extract Pygments CSS for dark theme syntax highlighting.

This script generates CSS for a specified Pygments theme and saves it
to docs/_static/pygments_dark.css for use in the documentation.

Usage:
    python extract_css.py [style_name]

Examples:
    python extract_css.py lightbulb
    python extract_css.py solarized-dark
    python extract_css.py github-dark
"""

import sys
from pathlib import Path
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles


def extract_pygments_css(style_name, output_file=None):
    """Extract Pygments CSS for the specified style, scoped to dark mode."""
    if output_file is None:
        output_file = Path("docs/_static/pygments_dark.css")

    # Validate the style exists
    available_styles = list(get_all_styles())
    if style_name not in available_styles:
        print(f"Error: Style '{style_name}' not found.")
        print(f"Available styles: {', '.join(sorted(available_styles))}")
        sys.exit(1)

    # Generate CSS for the specified style
    formatter = HtmlFormatter(style=style_name)
    css_content = formatter.get_style_defs('.highlight')

    # Wrap the CSS in a dark mode media query
    scoped_css = f"""/* Pygments {style_name} theme - only applied in dark mode */
@media (prefers-color-scheme: dark) {{
{css_content}
}}
"""

    # Write to file
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(scoped_css)

    print(f"Generated Pygments CSS for '{style_name}' theme (dark mode only): {output_file}")


if __name__ == "__main__":
    # Get style from command line argument or default to lightbulb
    if len(sys.argv) > 1:
        style_name = sys.argv[1]
    else:
        style_name = "lightbulb"

    extract_pygments_css(style_name)