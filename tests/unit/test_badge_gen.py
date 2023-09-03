# Copyright 2020 Lynn Root
"""Unit tests for interrogate/badge_gen.py module"""

import os
import sys

import pytest

from interrogate import badge_gen


HERE = os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir))
FIXTURES = os.path.join(HERE, "fixtures")
IS_WINDOWS = sys.platform in ("cygwin", "win32")


@pytest.mark.skipif(IS_WINDOWS, reason="unix-only tests")
@pytest.mark.parametrize(
    "out_format,out_file,exp_called_with",
    (
        (None, "fixtures/my_badge.svg", "fixtures/my_badge.svg"),
        ("svg", "fixtures/my_badge.svg", "fixtures/my_badge.svg"),
        ("png", "fixtures/my_badge.png", "fixtures/my_badge.tmp.svg"),
    ),
)
def test_save_badge(
    out_format, out_file, exp_called_with, mocker, monkeypatch
):
    """Badge is saved in the expected location."""
    mock_cairosvg = mocker.Mock()
    monkeypatch.setattr(badge_gen, "cairosvg", mock_cairosvg)

    mock_open = mocker.mock_open()
    m = mocker.patch("interrogate.badge_gen.open", mock_open)
    mock_rm = mocker.patch("interrogate.badge_gen.os.remove", mocker.Mock())

    badge_contents = "<svg>foo</svg>"

    actual = badge_gen.save_badge(badge_contents, out_file, out_format)
    assert out_file == actual
    m.assert_called_once_with(exp_called_with, "w")
    if out_format == "png":
        mock_cairosvg.svg2png.assert_called_once_with(
            url=exp_called_with, write_to=out_file, scale=2
        )
        mock_rm.assert_called_once_with(exp_called_with)


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
def test_save_badge_windows(mocker):
    """Badge is saved in the expected location."""
    mock_open = mocker.mock_open()
    m = mocker.patch("interrogate.badge_gen.open", mock_open)
    output = "C:\\foo\\bar\\my_badge.svg"
    badge_contents = "<svg>foo</svg>"

    actual = badge_gen.save_badge(badge_contents, output)
    assert output == actual
    m.assert_called_once_with(output, "w")


def test_save_badge_no_cairo(monkeypatch):
    """PNG can't be generated without extra dependencies installed."""
    monkeypatch.setattr("interrogate.badge_gen.cairosvg", None)
    badge_contents = "<svg>foo</svg>"

    with pytest.raises(ImportError, match="The required `cairosvg` "):
        badge_gen.save_badge(
            badge_contents, "fixtures/my_badge.png", output_format="png"
        )


def test_get_badge():
    """SVG badge is templated as expected."""
    actual = badge_gen.get_badge(99.9, "#4c1")
    actual = actual.replace("\n", "").replace("\r", "")
    expected_fixture = os.path.join(FIXTURES, "default-style", "99.svg")
    with open(expected_fixture) as f:
        expected = f.read()
        expected = expected.replace("\n", "").replace("\r", "")

    assert expected == actual


@pytest.mark.parametrize(
    "fixture,color,result,expected",
    (
        ("99.svg", "#4c1", 99.9, False),
        ("99.svg", "#97CA00", 99.9, True),
        ("99.svg", "#4c1", 80.0, True),
        ("does_not_exist.svg", "#4c1", 80.0, True),
        ("no_logo.svg", "#4c1", 99.9, True),
        ("99.png", None, None, True),
    ),
)
def test_should_generate(fixture, color, result, expected):
    """Only return True if existing badge needs updating"""
    output = os.path.join(FIXTURES, "default-style", fixture)
    actual = badge_gen.should_generate_badge(output, color, result)
    assert actual is expected


def test_should_generate_xml_error(mocker, monkeypatch):
    """Return True if parsing svg returns an error."""
    mock_minidom_parse = mocker.Mock()
    mock_minidom_parse.side_effect = Exception("fuuuu")
    monkeypatch.setattr(badge_gen.minidom, "parse", mock_minidom_parse)
    output = os.path.join(FIXTURES, "default-style", "99.svg")
    actual = badge_gen.should_generate_badge(output, "#123456", 99.9)
    assert actual is True


@pytest.mark.parametrize(
    "result,expected",
    (
        (0, "#e05d44"),
        (45, "#fe7d37"),
        (60, "#dfb317"),
        (89, "#a4a61d"),
        (90.0, "#97CA00"),
        (99.9, "#4c1"),
        (-1, "#9f9f9f"),
    ),
)
def test_get_color(result, expected):
    """Expected color returned according to results."""
    assert expected == badge_gen.get_color(result)


@pytest.mark.parametrize(
    "result,is_dir,should_generate,expected_fixture,out_format",
    (
        (100, True, True, "100.svg", None),
        (99.9, True, True, "99.svg", None),
        (90.0, True, True, "90.svg", None),
        (89.9, True, True, "89.svg", None),
        (60.0, True, True, "60.svg", None),
        (45.0, True, True, "45.svg", None),
        (0.0, True, True, "0.svg", None),
        (-1, True, True, "default.svg", None),
        (99.9, False, True, "99.svg", None),
        (99.9, False, False, "99.svg", None),
        # TODO: fixme: this fails on Github CI (ubuntu)
        # (99.9, True, True, "99.png", "png"),
    ),
)
@pytest.mark.parametrize(
    "style",
    (
        "plastic",
        "flat",
        "flat-square",
        "flat-square-modified",
        "for-the-badge",
        "social",
        None,
    ),
)
def test_create(
    result,
    is_dir,
    should_generate,
    expected_fixture,
    out_format,
    mocker,
    style,
    monkeypatch,
    tmpdir,
):
    """Status badges are created according to interrogation results."""
    monkeypatch.setattr(badge_gen.os.path, "isdir", lambda x: is_dir)
    output = tmpdir.mkdir("output")
    if not is_dir:
        output = output.join("badge.svg")

    if not should_generate:
        # pre-generate the badge
        mock_result = mocker.Mock(perc_covered=result)
        actual = badge_gen.create(str(output), mock_result, output_style=style)

    mock_result = mocker.Mock(perc_covered=result)
    actual = badge_gen.create(
        str(output), mock_result, out_format, output_style=style
    )

    flag = "rb" if out_format == "png" else "r"
    with open(actual, flag) as f:
        actual_contents = f.read()
        if out_format is None:
            actual_contents = actual_contents.replace("\n", "")

    if style is None:
        style = "default-style"
    expected_fixture = os.path.join(style, expected_fixture)
    expected_fixture = os.path.join(FIXTURES, expected_fixture)
    with open(expected_fixture, flag) as f:
        expected_contents = f.read()
        if out_format is None:
            expected_contents = expected_contents.replace("\n", "")

    assert expected_contents == actual_contents
