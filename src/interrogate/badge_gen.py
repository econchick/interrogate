# Copyright 2020 Lynn Root
"""Module for generating an SVG badge.

Inspired by `coverage-badge <https://github.com/dbrgn/coverage-badge>`_.
"""

import os

from pathlib import Path

import pkg_resources

from interrogate.utils import multiline_str_is_equal


DEFAULT_FILENAME = "interrogate_badge.svg"
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


def save_badge(badge, output):
    """Save badge to the specified path.

    :param str badge: SVG contents of badge.
    :param str output: path to output badge file.

    :return: path to output badge file.
    :rtype: str

    .. versionchanged:: 1.4.0 Badge only is written if content changes.
    """
    badge_path = Path(output)
    if not badge_path.suffixes:
        badge_path = badge_path / DEFAULT_FILENAME
    if not badge_path.is_file():
        badge_path.write_text(badge, encoding="utf8")
    elif not multiline_str_is_equal(
        badge_path.read_text(encoding="utf8"), badge
    ):
        badge_path.write_text(badge, encoding="utf8")

    return str(badge_path)


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


def create(output, result):
    """Create a status badge.

    :param str output: path to output badge file.
    :param coverage.InterrogateResults result: results of coverage
        interrogation.
    :return: path to output badge file.
    :rtype: str
    """
    result_perc = result.perc_covered
    color = get_color(result_perc)
    badge = get_badge(result_perc, color)
    return save_badge(badge, output)
