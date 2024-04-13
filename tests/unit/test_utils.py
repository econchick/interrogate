# Copyright 2020-2024 Lynn Root
"""Unit tests for interrogate/utils.py module"""

import re
import sys

import pytest

from interrogate import config, utils


IS_WINDOWS = sys.platform in ("cygwin", "win32")


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


@pytest.mark.skipif(IS_WINDOWS, reason="unix-only tests")
@pytest.mark.parametrize(
    "files,side_effect,expected",
    (
        (("/usr/src/app", "/usr/src/tests"), (True,), "/usr/src"),
        (
            ("/usr/src/app/sample.py", "/usr/src/app/sample2.py"),
            (False, True),
            "/usr/src/app",
        ),
        (("/usr/src/app/sample.py", "/usr/src/tests"), (True,), "/usr/src"),
        (("/usr/src/app", "/src/tests"), (True,), "/"),
    ),
)
def test_get_common_base(files, side_effect, expected, mocker, monkeypatch):
    """Return common base of a set of files/directories, if any."""
    mock_exists = mocker.Mock(side_effect=side_effect)
    monkeypatch.setattr(utils.pathlib.Path, "exists", mock_exists)
    actual = utils.get_common_base(files)
    assert expected == actual


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
@pytest.mark.parametrize(
    "files,side_effect,expected",
    (
        ((r"C:\usr\src\app", r"C:\usr\src\tests"), (True,), r"C:\usr\src"),
        (
            (r"C:\usr\src\app\sample.py", r"C:\usr\src\app\sample2.py"),
            (False, True),
            r"C:\usr\src\app",
        ),
        (
            (r"C:\usr\src\app\sample.py", r"C:\usr\src\tests"),
            (True,),
            r"C:\usr\src",
        ),
        ((r"C:\usr\src\app", r"C:\src\tests"), (True,), "C:\\"),
        (
            (r"C:\path\to\src\file.py", r"C:\path\to\tests\test_file.py"),
            (True,),
            r"C:\path\to",
        ),
    ),
)
def test_get_common_base_windows(
    files, side_effect, expected, mocker, monkeypatch
):
    """Return common base of a set of files/directories, if any."""
    mock_exists = mocker.Mock(side_effect=side_effect)
    monkeypatch.setattr(utils.pathlib.Path, "exists", mock_exists)
    actual = utils.get_common_base(files)
    assert expected == actual


@pytest.mark.parametrize(
    "color_conf,envvar,hasmarkup,expected",
    (
        # config color is set to false
        (False, None, None, False),
        # config color is set to True (must monkeypatch hasmarkup because
        # pytest messes with the `isatty` that's used in `py.io.
        # TerminalWriter().hasmarkup`)
        (True, None, True, True),
        # env var is set to skip color (must set config to true, but click
        # will override the config for us); envvars are always strings
        (True, "0", None, False),
        (True, "False", None, False),
        # env var is set to use color; must monkeypatch hasmarkup again
        (True, "True", True, True),
        (True, "1", True, True),
        # hasmarkup returns False
        (True, None, False, False),
        # hasmarkup returns True
        (True, None, True, True),
    ),
)
def test_output_formatter_should_markup(
    color_conf, envvar, hasmarkup, expected, monkeypatch
):
    """Expect markup unless configured (envvar or config) otherwise."""
    conf = config.InterrogateConfig(color=color_conf)
    formatter = utils.OutputFormatter(conf)
    if hasmarkup:
        monkeypatch.setattr(formatter.tw, "hasmarkup", hasmarkup)
    if envvar:
        monkeypatch.setenv("INTERROGATE_COLOR", envvar)

    assert expected == formatter.should_markup()


@pytest.mark.parametrize(
    "has_markup,padded_cells,expected_cells",
    (
        (True, ["foo", "bar"], ["foo", "bar"]),
        (False, ["foo", "MISSED"], ["foo", "MISSED"]),
        (
            True,
            ["foo", "MISSED"],
            ["\x1b[31mfoo\x1b[0m", "\x1b[31mMISSED\x1b[0m"],
        ),
        (
            True,
            ["foo", "COVERED"],
            ["\x1b[32mfoo\x1b[0m", "\x1b[32mCOVERED\x1b[0m"],
        ),
    ),
)
def test_output_formatter_set_detailed_markup(
    has_markup, padded_cells, expected_cells, monkeypatch
):
    """Detailed info is marked up with expected esc codes."""
    conf = config.InterrogateConfig()
    formatter = utils.OutputFormatter(conf)
    monkeypatch.setattr(formatter, "should_markup", lambda: has_markup)

    actual_cells = formatter.set_detailed_markup(padded_cells)

    assert expected_cells == actual_cells


@pytest.mark.parametrize(
    "has_markup,padded_cells,expected_cells",
    (
        (True, ["foo", "bar"], ["foo", "bar"]),
        (True, ["foo", "bar", "", "", ""], ["foo", "bar", "", "", ""]),
        (False, ["foo", "", "", "", "100%"], ["foo", "", "", "", "100%"]),
        (
            True,
            ["foo", "", "", "", "100%"],
            [
                "\x1b[32mfoo\x1b[0m",
                "\x1b[32m\x1b[0m",
                "\x1b[32m\x1b[0m",
                "\x1b[32m\x1b[0m",
                "\x1b[32m100%\x1b[0m",
            ],
        ),
        (
            True,
            ["foo", "", "", "", "60%"],
            [
                "\x1b[31mfoo\x1b[0m",
                "\x1b[31m\x1b[0m",
                "\x1b[31m\x1b[0m",
                "\x1b[31m\x1b[0m",
                "\x1b[31m60%\x1b[0m",
            ],
        ),
    ),
)
def test_output_formatter_set_summary_markup(
    has_markup, padded_cells, expected_cells, monkeypatch
):
    """Summary info is marked up with expected esc codes."""
    conf = config.InterrogateConfig()
    formatter = utils.OutputFormatter(conf)
    monkeypatch.setattr(formatter, "should_markup", lambda: has_markup)

    actual_cells = formatter.set_summary_markup(padded_cells)

    assert expected_cells == actual_cells


@pytest.mark.skipif(IS_WINDOWS, reason="unix-only tests")
@pytest.mark.parametrize(
    "table_type,padded_cells,colwidths,colaligns,width,expected",
    (
        # no data
        ("summary", [""], [0], ["left"], 15, "|             |"),
        ("detailed", [""], [0], ["left"], 15, "|             |"),
        ("not_a_type", [""], [0], ["left"], 15, "|             |"),
        # left & right align
        (
            "summary",
            ["foo", "bar"],
            [3, 3],
            ["left", "right"],
            15,
            "|foo   |   bar|",
        ),
        # left & right align with a non-equal amount of padding per column
        (
            "summary",
            ["foo", "bar"],
            [3, 3],
            ["left", "right"],
            14,
            "|foo   |  bar|",
        ),
        # table separator
        (
            "summary",
            ["---", ""],
            [3, 0],
            ["left", "right"],
            15,
            "|--------|----|",
        ),
        # default to left alignment
        ("summary", ["foo", "bar"], [3, 3], ["?", "?"], 15, "|foo   |bar   |"),
    ),
)
def test_output_formatter_interrogate_line_formatter(
    table_type,
    padded_cells,
    colwidths,
    colaligns,
    width,
    expected,
    monkeypatch,
):
    """Data is padded and aligned correctly to fit the terminal width."""
    conf = config.InterrogateConfig(color=False)
    formatter = utils.OutputFormatter(conf)
    monkeypatch.setattr(formatter, "TERMINAL_WIDTH", width)

    actual = formatter._interrogate_line_formatter(
        padded_cells, colwidths, colaligns, table_type=table_type
    )

    assert width == len(actual)
    assert expected == actual


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
@pytest.mark.parametrize(
    "table_type,padded_cells,colwidths,colaligns,width,expected",
    (
        # no data
        ("summary", [""], [0], ["left"], 15, "|            |"),
        ("detailed", [""], [0], ["left"], 15, "|            |"),
        ("not_a_type", [""], [0], ["left"], 15, "|            |"),
        # left & right align
        (
            "summary",
            ["foo", "bar"],
            [3, 3],
            ["left", "right"],
            15,
            "|foo   |  bar|",
        ),
        # left & right align with a non-equal amount of padding per column
        (
            "summary",
            ["foo", "bar"],
            [3, 3],
            ["left", "right"],
            14,
            "|foo  |  bar|",
        ),
        # table separator
        (
            "summary",
            ["---", ""],
            [3, 0],
            ["left", "right"],
            15,
            "|-------|----|",
        ),
        # default to left alignment
        ("summary", ["foo", "bar"], [3, 3], ["?", "?"], 15, "|foo   |bar  |"),
    ),
)
def test_output_formatter_interrogate_line_formatter_windows(
    table_type,
    padded_cells,
    colwidths,
    colaligns,
    width,
    expected,
    monkeypatch,
):
    """Data is padded and aligned correctly to fit the terminal width."""
    conf = config.InterrogateConfig(color=False)
    formatter = utils.OutputFormatter(conf)
    monkeypatch.setattr(formatter, "TERMINAL_WIDTH", width)

    actual = formatter._interrogate_line_formatter(
        padded_cells, colwidths, colaligns, table_type=table_type
    )

    assert width - 1 == len(actual)
    assert expected == actual


@pytest.mark.parametrize("table_type", ("detailed", "summary"))
def test_output_formatter_get_table_formatter(table_type, mocker, monkeypatch):
    """The returned table formatter uses the correct table type."""
    mock_table_format = mocker.Mock()
    monkeypatch.setattr(utils.tabulate, "TableFormat", mock_table_format)

    conf = config.InterrogateConfig()
    formatter = utils.OutputFormatter(conf)
    formatter.get_table_formatter(table_type=table_type)

    mock_table_format.assert_called_once()


def test_output_formatter_get_table_formatter_raises():
    """Raise if received an table type other than 'detailed' or 'summary'."""
    conf = config.InterrogateConfig()
    formatter = utils.OutputFormatter(conf)
    with pytest.raises(AssertionError):
        formatter.get_table_formatter(table_type="not_a_type")
