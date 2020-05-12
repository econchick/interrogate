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
    "output,is_dir,expected",
    (
        ("foo/bar", True, "foo/bar/interrogate_badge.svg"),
        ("foo/bar/my_badge.svg", False, "foo/bar/my_badge.svg"),
    ),
)
def test_save_badge(output, is_dir, expected, mocker, monkeypatch):
    """Badge is saved in the expected location."""
    monkeypatch.setattr(badge_gen.os.path, "isdir", lambda x: is_dir)

    mock_open = mocker.mock_open()
    m = mocker.patch("interrogate.badge_gen.open", mock_open)

    badge_contents = "<svg>foo</svg>"

    actual = badge_gen.save_badge(badge_contents, output)
    assert expected == actual
    m.assert_called_once_with(expected, "w")


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
@pytest.mark.parametrize(
    "output,is_dir,expected",
    (
        ("C:\\foo\\bar", True, "C:\\foo\\bar\\interrogate_badge.svg"),
        ("C:\\foo\\bar\\my_badge.svg", False, "C:\\foo\\bar\\my_badge.svg"),
    ),
)
def test_save_badge_windows(output, is_dir, expected, mocker, monkeypatch):
    """Badge is saved in the expected location."""
    monkeypatch.setattr(badge_gen.os.path, "isdir", lambda x: is_dir)

    mock_open = mocker.mock_open()
    m = mocker.patch("interrogate.badge_gen.open", mock_open)

    badge_contents = "<svg>foo</svg>"

    actual = badge_gen.save_badge(badge_contents, output)
    assert expected == actual
    m.assert_called_once_with(expected, "w")


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
    "result,expected_fixture",
    (
        (99.9, "99.svg"),
        (90.0, "90.svg"),
        (89.9, "89.svg"),
        (60.0, "60.svg"),
        (45.0, "45.svg"),
        (0.0, "0.svg"),
        (-1, "default.svg"),
    ),
)
def test_create(result, expected_fixture, mocker, monkeypatch, tmpdir):
    """Status badges are created according to interrogation results."""
    mock_result = mocker.Mock(perc_covered=result)
    actual = badge_gen.create(str(tmpdir), mock_result)

    with open(actual, "r") as f:
        actual_contents = f.read()
        actual_contents = actual_contents.replace("\n", "")

    expected_fixture = os.path.join(FIXTURES, expected_fixture)
    with open(expected_fixture, "r") as f:
        expected_contents = f.read()
        expected_contents = expected_contents.replace("\n", "")

    assert expected_contents == actual_contents
