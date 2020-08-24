# Copyright 2020 Lynn Root
"""Unit tests for interrogate/badge_gen.py module"""

import os
import sys

from pathlib import Path

import pytest

from interrogate import badge_gen


HERE = os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir))
FIXTURES = os.path.join(HERE, "fixtures")
IS_WINDOWS = sys.platform in ("cygwin", "win32")


def body_test_save_badge(
    output, expected, file_exists, expected_read, mocker, monkeypatch,
):
    """Function body of test_save_badge and test_save_badge_windows"""
    monkeypatch.setattr(Path, "is_file", lambda x: file_exists)
    mock_read_text = mocker.Mock(return_value=expected_read)
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    mock_write_text = mocker.Mock(return_value=None)
    monkeypatch.setattr(Path, "write_text", mock_write_text)
    badge_contents = "<svg>foo</svg>"
    actual = badge_gen.save_badge(badge_contents, output)
    assert expected == actual

    if file_exists:
        mock_read_text.assert_called_once_with(encoding="utf8")
        if expected_read == badge_contents:
            mock_write_text.assert_not_called()
        else:
            mock_write_text.assert_called_once_with(
                badge_contents, encoding="utf8"
            )

    else:
        mock_read_text.assert_not_called()
        mock_write_text.assert_called_once_with(
            badge_contents, encoding="utf8"
        )


@pytest.mark.skipif(IS_WINDOWS, reason="unix-only tests")
@pytest.mark.parametrize(
    "expected_read", ["<svg>foo</svg>", "<svg>foo2</svg>"]
)
@pytest.mark.parametrize("file_exists", [True, False])
@pytest.mark.parametrize(
    "output,expected",
    (
        ("foo/bar", "foo/bar/interrogate_badge.svg"),
        ("foo/bar/my_badge.svg", "foo/bar/my_badge.svg"),
    ),
)
def test_save_badge(
    output, expected, file_exists, expected_read, mocker, monkeypatch
):
    """Badge is saved in the expected location."""
    body_test_save_badge(
        output, expected, file_exists, expected_read, mocker, monkeypatch
    )


@pytest.mark.skipif(not IS_WINDOWS, reason="windows-only tests")
@pytest.mark.parametrize(
    "expected_read", ["<svg>foo</svg>", "<svg>foo2</svg>"]
)
@pytest.mark.parametrize("file_exists", [True, False])
@pytest.mark.parametrize(
    "output,expected",
    (
        ("C:\\foo\\bar", "C:\\foo\\bar\\interrogate_badge.svg"),
        ("C:\\foo\\bar\\my_badge.svg", "C:\\foo\\bar\\my_badge.svg"),
    ),
)
def test_save_badge_windows(
    output, expected, file_exists, expected_read, mocker, monkeypatch
):
    """Badge is saved in the expected location."""
    body_test_save_badge(
        output, expected, file_exists, expected_read, mocker, monkeypatch
    )


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
