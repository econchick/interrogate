# Copyright 2020 Lynn Root
"""Module for generating an SVG badge.

Inspired by `coverage-badge <https://github.com/dbrgn/coverage-badge>`_.
"""

import os
import sys

from importlib import resources
from xml.dom import minidom


try:
    import cairosvg
except ImportError:  # pragma: no cover
    cairosvg = None


DEFAULT_FILENAME = "interrogate_badge"
COLORS = {
    "brightgreen": "#4c1",
    "green": "#97CA00",
    "yellowgreen": "#a4a61d",
    "yellow": "#dfb317",
    "orange": "#fe7d37",
    "red": "#e05d44",
    "lightgrey": "#9f9f9f",
}

COLOR_RANGES = [
    (95, "brightgreen"),
    (90, "green"),
    (75, "yellowgreen"),
    (60, "yellow"),
    (40, "orange"),
    (0, "red"),
]
SUPPORTED_OUTPUT_FORMATS = ["svg", "png"]
# depending on the character length of the result (e.g. 100, 99.9, 9.9)
# a few values in the svg template need to adjust so it's readable.
# Tuple of values: (svg_width, rect_width, text_x, text_length)
SVG_WIDTH_VALUES = {
    # integer
    "100": {
        "plastic": (135, 43, 1140, 330),
        "social": (133, 37, 1140, 290),
        "flat": (114, 43, 915, 330),
        "flat-square": (135, 42, 1140, 330),
        "flat-square-modified": (114, 43, 915, 330),
        "for-the-badge": (0, 0, 1670.75, 390),
    },
    # 10.0 - 99.9, float
    "99.9": {
        "plastic": (135, 43, 1140, 370),
        "social": (137, 41, 1175, 330),
        "flat": (118, 47, 935, 370),
        "flat-square": (140, 47, 1160, 370),
        "flat-square-modified": (114, 43, 915, 370),
        "for-the-badge": (0, 0, 1660.75, 432.5),
    },
    # <= 9.9, float
    "9.9": {
        "plastic": (135, 43, 1140, 290),
        "social": (131, 35, 1145, 270),
        "flat": (110, 39, 895, 290),
        "flat-square": (132, 39, 1120, 290),
        "flat-square-modified": (114, 43, 915, 300),
        "for-the-badge": (0, 0, 1680.75, 350),
    },
}


def save_badge(badge, output, output_format=None):
    """Save badge to the specified path.

    .. versionadded:: 1.4.0 new ``output_format`` keyword argument

    :param str badge: SVG contents of badge.
    :param str output: path to output badge file.
    :param str output_format: format for output; either ``svg`` or
        ``png``. Defaults to ``svg``.
    :return: path to output badge file.
    :rtype: str
    """
    if output_format is None:
        output_format = "svg"

    if output_format == "svg":
        with open(output, "w") as f:
            f.write(badge)

        return output

    if cairosvg is None:
        raise ImportError(
            "The required `cairosvg` dependency in order to generate a PNG "
            "file was not found. Please install `interrogate[png]`."
        )

    # need to write the badge as an svg first in order to convert it to
    # another format
    tmp_output_file = f"{os.path.splitext(output)[0]}.tmp.svg"
    try:
        with open(tmp_output_file, "w") as f:
            f.write(badge)

        cairosvg.svg2png(url=tmp_output_file, write_to=output, scale=2)

    finally:
        try:
            os.remove(tmp_output_file)
        except Exception:  # pragma: no cover
            pass

    return output


def _get_badge_measurements(result, style):
    """Lookup templated style values based on result number."""
    if result == 100:
        width_values = SVG_WIDTH_VALUES["100"]
    elif result >= 10:
        width_values = SVG_WIDTH_VALUES["99.9"]
    else:
        width_values = SVG_WIDTH_VALUES["9.9"]
    style_width_values = width_values[style]
    return {
        "svg_width": style_width_values[0],
        "rect_width": style_width_values[1],
        "text_x": style_width_values[2],
        "text_length": style_width_values[3],
    }


def _format_result(result):
    """Format result into string for templating."""
    # do not include decimal if it's 100
    if result == 100:
        return "100"
    return f"{result:.1f}"


def get_badge(result, color, style=None):
    """Generate an SVG from template.

    :param float result: coverage % result.
    :param str color: color of badge.

    :return: SVG contents of badge.
    :rtype: str
    """
    if style is None:
        style = "flat-square-modified"
    template_file = f"{style}-style.svg"
    badge_template_values = _get_badge_measurements(result, style)
    result = _format_result(result)
    badge_template_values["result"] = result
    badge_template_values["color"] = color

    if sys.version_info >= (3, 9):
        tmpl = (
            resources.files("interrogate") / "badge" / template_file
        ).read_text()
    else:
        with resources.path("interrogate", "badge") as p:
            tmpl = (p / template_file).read_text()

    for key, value in badge_template_values.items():
        tmpl = tmpl.replace("{{ %s }}" % key, str(value))
    return tmpl


def should_generate_badge(output, color, result):
    """Detect if existing badge needs updating.

    This is to help avoid unnecessary newline updates. See
    https://github.com/econchick/interrogate/issues/40

    .. caution::

        A badge will always be generated for PNG format.

    .. versionadded:: 1.3.1 Function added
    .. versionchanged:: 1.3.2 Added logo to badge, so regenerate badge if
        logo doesn't exist.

    :param str output: path to output badge file
    :param float result: coverage % result.
    :param str color: color of badge.
    :return: Whether or not the badge SVG file should be generated.
    :rtype: bool
    """
    if not os.path.exists(output):
        return True

    if not output.endswith(".svg"):
        return True

    try:
        badge = minidom.parse(output)
    except Exception:
        # an exception might happen when a file is not an SVG file but has
        # `.svg` extension (perhaps a png image was generated with the wrong
        # file extension, for example)
        return True

    # added the sloth logo in 1.3.2 - if it doesn't exist, we should
    # go ahead and recreate the badge
    gs = badge.getElementsByTagName("g")
    gids = [g.getAttribute("id") for g in gs]
    if "logo-pink" not in gids:
        return True

    rects = badge.getElementsByTagName("rect")
    current_colors = [
        r.getAttribute("style")
        for r in rects
        if r.hasAttribute("data-interrogate")
    ]
    fill_color = f"fill:{color}"
    if fill_color not in current_colors:
        return True

    texts = badge.getElementsByTagName("text")
    current_results = [
        t.childNodes[0].data
        for t in texts
        if t.hasAttribute("data-interrogate")
    ]
    result = f"{result:.1f}%"
    if result in current_results:
        return False
    return True


def get_color(result):
    """Get color for current doc coverage percent.

    :param float result: coverage % result
    :return: color of badge according to coverage completeness.
    :rtype: str
    """
    for minimum, color in COLOR_RANGES:
        if result >= minimum:
            return COLORS[color]
    return COLORS["lightgrey"]


def create(output, result, output_format=None, output_style=None):
    """Create a status badge.

    The badge file will only be written if it doesn't exist, or if the
    existing badge file does not require any updates.

    .. versionchanged:: 1.3.1 Only generate badge file if its contents
        change.
    .. versionadded:: 1.4.0 Optional ``output_format`` keyword to support
        file types other than SVG.
    .. versionadded:: 1.5.0 Optional ``output_style`` keyword to support
        different styles of the shields.io badge.

    :param str output: path to output badge file.
    :param coverage.InterrogateResults result: results of coverage
        interrogation.
    :return: path to output badge file.
    :rtype: str
    """
    if output_format is None:
        output_format = "svg"
    if os.path.isdir(output):
        filename = DEFAULT_FILENAME + "." + output_format
        output = os.path.join(output, filename)

    result_perc = result.perc_covered
    color = get_color(result_perc)

    should_generate = should_generate_badge(output, color, result_perc)
    if should_generate:
        badge = get_badge(result_perc, color, output_style)
        return save_badge(badge, output, output_format)
    return output
