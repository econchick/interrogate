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
def test_save_badge(mocker):
    """Badge is saved in the expected location."""
    mock_open = mocker.mock_open()
    m = mocker.patch("interrogate.badge_gen.open", mock_open)
    output = "foo/bar/my_badge.svg"
    badge_contents = "<svg>foo</svg>"

    actual = badge_gen.save_badge(badge_contents, output)
    assert output == actual
    m.assert_called_once_with(output, "w")


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


def test_get_badge():
    """SVG badge is templated as expected."""
    actual = badge_gen.get_badge(99.9, "#4c1")
    actual = actual.replace("\n", "").replace("\r", "")
    expected_fixture = os.path.join(FIXTURES, "99.svg")
    with open(expected_fixture, "r") as f:
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
    ),
)
def test_should_generate(fixture, color, result, expected):
    """Only return True if existing badge needs updating"""
    output = os.path.join(FIXTURES, fixture)
    actual = badge_gen.should_generate_badge(output, color, result)
    assert actual is expected


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
    "result,is_dir,should_generate,expected_fixture",
    (
        (99.9, True, True, "99.svg"),
        (90.0, True, True, "90.svg"),
        (89.9, True, True, "89.svg"),
        (60.0, True, True, "60.svg"),
        (45.0, True, True, "45.svg"),
        (0.0, True, True, "0.svg"),
        (-1, True, True, "default.svg"),
        (99.9, False, True, "99.svg"),
        (99.9, False, False, "99.svg"),
    ),
)
def test_create(
    result,
    is_dir,
    should_generate,
    expected_fixture,
    mocker,
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
        actual = badge_gen.create(str(output), mock_result)

    mock_result = mocker.Mock(perc_covered=result)
    actual = badge_gen.create(str(output), mock_result)

    with open(actual, "r") as f:
        actual_contents = f.read()
        actual_contents = actual_contents.replace("\n", "")

    expected_fixture = os.path.join(FIXTURES, expected_fixture)
    with open(expected_fixture, "r") as f:
        expected_contents = f.read()
        expected_contents = expected_contents.replace("\n", "")

    assert expected_contents == actual_contents
