# Copyright 2020 Lynn Root
"""Functional tests for interrogate/coverage.py."""

import os
import sys

import pytest

from interrogate import config
from interrogate import coverage


HERE = os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir))
SAMPLE_DIR = os.path.join(HERE, "sample")
FIXTURES = os.path.join(HERE, "fixtures")
IS_WINDOWS = sys.platform in ("cygwin", "win32")


@pytest.mark.parametrize(
    "paths,conf,exp_results",
    (
        ([os.path.join(SAMPLE_DIR, "empty.py"),], {}, (1, 0, 1, "0.0")),
        (
            [os.path.join(SAMPLE_DIR, "empty.py"),],
            {"ignore_module": True},
            (0, 0, 0, "0.0"),
        ),
        ([SAMPLE_DIR,], {}, (56, 26, 30, "46.4")),
        ([os.path.join(SAMPLE_DIR, "partial.py")], {}, (22, 7, 15, "31.8")),
        (
            [os.path.join(SAMPLE_DIR, "full.py"),],
            {"ignore_nested_functions": True},
            (17, 17, 0, "100.0"),
        ),
        (
            [os.path.join(SAMPLE_DIR, "partial.py"),],
            {"ignore_nested_functions": True},
            (20, 6, 14, "30.0"),
        ),
    ),
)
def test_coverage_simple(paths, conf, exp_results, mocker):
    """Happy path - get expected results given a file or directory"""
    conf = config.InterrogateConfig(**conf)
    interrogate_coverage = coverage.InterrogateCoverage(paths=paths, conf=conf)

    results = interrogate_coverage.get_coverage()

    assert exp_results[0] == results.total
    assert exp_results[1] == results.covered
    assert exp_results[2] == results.missing
    assert exp_results[3] == "{:.1f}".format(results.perc_covered)


def test_coverage_errors(capsys):
    """Exit when no Python files are found."""
    path = os.path.join(SAMPLE_DIR, "ignoreme.txt")
    interrogate_coverage = coverage.InterrogateCoverage(paths=[path])

    with pytest.raises(SystemExit, match="1"):
        interrogate_coverage.get_coverage()

    captured = capsys.readouterr()
    assert "E: Invalid file" in captured.err

    interrogate_coverage = coverage.InterrogateCoverage(paths=[FIXTURES])

    with pytest.raises(SystemExit, match="1"):
        interrogate_coverage.get_coverage()

    captured = capsys.readouterr()
    assert "E: No Python files found to interrogate in " in captured.err


@pytest.mark.parametrize(
    "level,exp_fixture_file",
    (
        # (0, "expected_no_verbosity.txt"),
        # (1, "expected_summary.txt"),
        (2, "expected_detailed.txt"),
    ),
)
def test_print_results(level, exp_fixture_file, capsys, monkeypatch):
    """Output of test results differ by verbosity."""
    monkeypatch.setattr(coverage.utils.OutputFormatter, "TERMINAL_WIDTH", 80)

    interrogate_coverage = coverage.InterrogateCoverage(paths=[SAMPLE_DIR])
    results = interrogate_coverage.get_coverage()
    interrogate_coverage.print_results(
        results=results, output=None, verbosity=level
    )

    captured = capsys.readouterr()
    expected_fixture = os.path.join(FIXTURES, exp_fixture_file)
    if IS_WINDOWS:
        expected_fixture = os.path.join(FIXTURES, "windows", exp_fixture_file)
    with open(expected_fixture, "r") as f:
        expected_out = f.read()

    print("expected")
    print(expected_out)
    print("-----")
    print("actual")
    print(captured.out)
    assert expected_out in captured.out


@pytest.mark.parametrize(
    "ignore_module,level,exp_fixture_file",
    (
        (False, 2, "expected_detailed.txt"),
        (True, 2, "expected_detailed_no_module.txt"),
        (False, 1, "expected_summary.txt"),
        (True, 1, "expected_summary_no_module.txt"),
    ),
)
def test_print_results_ignore_module(
    ignore_module, level, exp_fixture_file, capsys, monkeypatch
):
    """Do not print module info if ignore_module is True."""
    monkeypatch.setattr(coverage.utils.OutputFormatter, "TERMINAL_WIDTH", 80)

    conf = {"ignore_module": ignore_module}
    conf = config.InterrogateConfig(**conf)

    interrogate_coverage = coverage.InterrogateCoverage(
        paths=[SAMPLE_DIR], conf=conf
    )
    results = interrogate_coverage.get_coverage()
    interrogate_coverage.print_results(
        results=results, output=None, verbosity=level
    )

    captured = capsys.readouterr()
    expected_fixture = os.path.join(FIXTURES, exp_fixture_file)
    if IS_WINDOWS:
        expected_fixture = os.path.join(FIXTURES, "windows", exp_fixture_file)
    with open(expected_fixture, "r") as f:
        expected_out = f.read()

    assert expected_out in captured.out


def test_print_results_single_file(capsys, monkeypatch):
    """Results for a single file should still list the filename."""

    monkeypatch.setattr(coverage.utils.OutputFormatter, "TERMINAL_WIDTH", 80)
    single_file = os.path.join(SAMPLE_DIR, "full.py")
    interrogate_coverage = coverage.InterrogateCoverage(paths=[single_file])
    results = interrogate_coverage.get_coverage()
    interrogate_coverage.print_results(
        results=results, output=None, verbosity=2
    )

    captured = capsys.readouterr()
    expected_fixture = os.path.join(
        FIXTURES, "expected_detailed_single_file.txt"
    )

    if IS_WINDOWS:
        expected_fixture = os.path.join(
            FIXTURES, "windows", "expected_detailed_single_file.txt"
        )

    with open(expected_fixture, "r") as f:
        expected_out = f.read()

    assert expected_out in captured.out
    # I don't want to deal with path mocking out just to get tests to run
    # everywhere
    if not IS_WINDOWS:
        assert "tests/functional/sample/" in captured.out
        assert "tests/functional/sample/full.py" not in captured.out
    else:
        assert "tests\\functional\\sample\\" in captured.out
        assert "tests\\functional\\sample\\full.py" not in captured.out
