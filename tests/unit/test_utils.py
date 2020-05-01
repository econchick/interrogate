# Copyright 2020 Lynn Root
"""Unit tests for interrogate/utils.py module"""

import re
import sys

import pytest

from interrogate import utils


@pytest.mark.parametrize(
    "value,exp",
    (
        # no regex given
        (None, None),
        ((), None),
        # single regex
        (["^_.*"], [re.compile("^_.*")]),
        # multiple regexes
        (
            ["^get_.*", "^post_.*"],
            [re.compile("^get_.*"), re.compile("^post_.*")],
        ),
    ),
)
def test_parse_regex(value, exp):
    """Compile a given string into regex."""
    actual = utils.parse_regex({}, "ignore_regex", value)
    assert exp == actual


@pytest.mark.parametrize("filename", (None, "-", "input.txt"))
def test_smart_open(filename, mocker):
    """Handles both opening a file and stdout in the same manner."""
    m_open = mocker.mock_open()
    mock_open = mocker.patch("interrogate.utils.open", m_open)

    with utils.smart_open(filename, fmode="r") as act_ret:
        pass

    if filename and filename != "-":
        mock_open.assert_called_once_with(filename, "r")
        assert act_ret.closed
    else:
        mock_open.assert_not_called()
        assert act_ret == sys.stdout


@pytest.mark.parametrize(
    "files,expected",
    (
        (("/usr/src/app", "/usr/src/tests"), "/usr/src"),
        (("/usr/src/app/sample.py", "/usr/src/tests"), "/usr/src"),
        (("/usr/src/app", "/src/tests"), ""),
    ),
)
def test_get_common_base(files, expected):
    """Return common base of a set of files/directories, if any."""
    actual = utils.get_common_base(files)
    assert expected == actual


@pytest.mark.parametrize(
    "padded_cells,colwidths,colaligns,expected",
    (
        # no data
        ([""], [1], ["left"], "|             |"),
        # left & right align
        (["foo", "bar"], [7, 7], ["left", "right"], "|foo  |  bar|"),
        # table separator
        (["---", ""], [7, 7], ["left", "right"], "|-------|----|"),
        # default to left alignment
        (["foo", "bar"], [7, 7], ["center", "center"], "|foo  |bar  |"),
    ),
)
def test_interrogate_line_formatter(
    padded_cells, colwidths, colaligns, expected, monkeypatch
):
    """Data is padded and aligned correctly to fit the terminal width."""
    monkeypatch.setattr(utils, "TERMINAL_WIDTH", 15)

    actual = utils.interrogate_line_formatter(
        padded_cells, colwidths, colaligns
    )

    assert expected == actual
    assert 15 >= len(actual)
