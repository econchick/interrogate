# Copyright 2020 Lynn Root
"""Module for generating an SVG badge.

Inspired by `coverage-badge <https://github.com/dbrgn/coverage-badge>`_.
"""

import os

from xml.dom import minidom

import pkg_resources


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


def get_badge(result, color):
    """Generate an SVG from template.

    :param float result: coverage % result.
    :param str color: color of badge.

    :return: SVG contents of badge.
    :rtype: str
    """
    result = "{:.1f}".format(result)
    template_path = os.path.join("badge", "template.svg")
    tmpl = pkg_resources.resource_string(__name__, template_path)
    tmpl = tmpl.decode("utf8")
    return tmpl.replace("{{ result }}", result).replace("{{ color }}", color)


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

    badge = minidom.parse(output)

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
    fill_color = "fill:{}".format(color)
    if fill_color not in current_colors:
        return True

    texts = badge.getElementsByTagName("text")
    current_results = [
        t.childNodes[0].data
        for t in texts
        if t.hasAttribute("data-interrogate")
    ]
    result = "{:.1f}%".format(result)
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


def create(output, result, output_format=None):
    """Create a status badge.

    The badge file will only be written if it doesn't exist, or if the
    existing badge file does not require any updates.

    .. versionchanged:: 1.3.1 Only generate badge file if its contents
        change.
    .. versionadded:: 1.4.0 Optional ``output_format`` keyword to support
        file types other than SVG.

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
        badge = get_badge(result_perc, color)
        return save_badge(badge, output, output_format)
    return output
