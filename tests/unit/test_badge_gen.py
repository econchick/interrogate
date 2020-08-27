# Copyright 2020 Lynn Root
"""Unit tests for interrogate/badge_gen.py module"""

import sys

from pathlib import Path

import pytest

from interrogate import badge_gen
from interrogate.utils import multiline_str_is_equal


HERE = Path(__file__).absolute().parent
FIXTURES = HERE / "fixtures"


if sys.platform in ("cygwin", "win32"):
    SAVE_BADGE_TEST_PATHS = (
        ("C:\\foo\\bar", "C:\\foo\\bar\\interrogate_badge.svg"),
        ("C:\\foo\\bar\\my_badge.svg", "C:\\foo\\bar\\my_badge.svg"),
    )
else:
    SAVE_BADGE_TEST_PATHS = (
        ("foo/bar", "foo/bar/interrogate_badge.svg"),
        ("foo/bar/my_badge.svg", "foo/bar/my_badge.svg"),
    )


@pytest.mark.parametrize(
    "expected_read", ["<svg>foo</svg>", "<svg>foo2</svg>"]
)
@pytest.mark.parametrize("file_exists", [True, False])
@pytest.mark.parametrize("output,expected", SAVE_BADGE_TEST_PATHS)
def test_save_badge(
    output, expected, file_exists, expected_read, mocker, monkeypatch
):
    """Badge is saved in the expected location."""
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


def test_get_badge():
    """SVG badge is templated as expected."""
    actual = badge_gen.get_badge(99.9, "#4c1")

    expected_fixture = FIXTURES / "99.svg"
    expected = expected_fixture.read_text()

    assert multiline_str_is_equal(expected, actual)


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
    actual_contents = Path(actual).read_text()

    expected_fixture = FIXTURES / expected_fixture
    expected_contents = expected_fixture.read_text()

    assert multiline_str_is_equal(expected_contents, actual_contents)
