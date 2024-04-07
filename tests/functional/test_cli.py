# Copyright 2020 Lynn Root
"""Functional tests for the CLI and implicitly interrogate/visit.py."""

import os
import sys

import pytest

from click import testing

from interrogate import cli
from interrogate import config


HERE = os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir))
SAMPLE_DIR = os.path.join(HERE, "sample")
FIXTURES = os.path.join(HERE, "fixtures")
IS_WINDOWS = sys.platform in ("cygwin", "win32")


@pytest.fixture
def runner(monkeypatch):
    """Click fixture runner"""
    # don't let the tests accidentally bring in the project's own
    # pyproject.toml
    monkeypatch.setattr(config, "find_project_config", lambda x: None)
    return testing.CliRunner()


def test_run_no_paths(runner, monkeypatch, tmpdir):
    """Assume current working directory if no paths are given."""
    monkeypatch.setattr(os, "getcwd", lambda: SAMPLE_DIR)

    result = runner.invoke(cli.main, [])

    assert "actual: 51.4%" in result.output
    assert 1 == result.exit_code


@pytest.mark.parametrize(
    "flags,exp_result,exp_exit_code",
    (
        # no flags
        ([], 51.4, 1),
        # ignore init module
        (["-I"], 51.4, 1),
        # ignore module docs
        (["-M"], 51.5, 1),
        # ignore semiprivate docs
        (["-s"], 52.2, 1),
        # ignore private docs
        (["-p"], 52.9, 1),
        # ignore property getter/setter/deleter decorators
        (["-P"], 50.0, 1),
        # ignore property setter decorators
        (["-S"], 51.4, 1),
        # ignore magic method docs
        (["-m"], 51.4, 1),
        # ignore init method docs
        (["-i"], 50.7, 1),
        # ignore nested funcs
        (["-n"], 50.7, 1),
        # ignore nested classes
        (["-C"], 52.1, 1),
        # ignore @typing.overload-decorated functions
        (["-O"], 51.5, 1),
        # ignore regex
        (["-r", "^get$"], 51.4, 1),
        # whitelist regex
        (["-w", "^get$"], 50.0, 1),
        # exclude file
        (["-e", os.path.join(SAMPLE_DIR, "partial.py")], 62.2, 1),
        # exclude file which doesn't exist
        (["-e", os.path.join(SAMPLE_DIR, "does.not.exist")], 51.4, 1),
        # fail under
        (["-f", "40"], 51.4, 0),
    ),
)
def test_run_shortflags(flags, exp_result, exp_exit_code, runner):
    """Test CLI with single short flags"""
    cli_inputs = flags + [SAMPLE_DIR]
    result = runner.invoke(cli.main, cli_inputs)

    exp_partial_output = f"actual: {exp_result:.1f}%"
    assert exp_partial_output in result.output
    assert exp_exit_code == result.exit_code


@pytest.mark.parametrize(
    "flags,exp_result,exp_exit_code",
    (
        (["--ignore-init-module"], 51.4, 1),
        (["--ignore-module"], 51.5, 1),
        (["--ignore-semiprivate"], 52.2, 1),
        (["--ignore-private"], 52.9, 1),
        (["--ignore-property-decorators"], 50.0, 1),
        (["--ignore-setters"], 51.4, 1),
        (["--ignore-magic"], 51.4, 1),
        (["--ignore-init-method"], 50.7, 1),
        (["--ignore-nested-functions"], 50.7, 1),
        (["--ignore-nested-classes"], 52.1, 1),
        (["--ignore-overloaded-functions"], 51.5, 1),
        (["--ignore-regex", "^get$"], 51.4, 1),
        (["--ext", "pyi"], 63.1, 1),
        (["--whitelist-regex", "^get$"], 50.0, 1),
        (["--exclude", os.path.join(SAMPLE_DIR, "partial.py")], 62.2, 1),
        (["--fail-under", "40"], 51.4, 0),
        (["--style", "google"], 54.1, 1),
    ),
)
def test_run_longflags(flags, exp_result, exp_exit_code, runner):
    """Test CLI with single long flags"""
    cli_inputs = flags + [SAMPLE_DIR]
    result = runner.invoke(cli.main, cli_inputs)

    exp_partial_output = f"actual: {exp_result:.1f}%"
    assert exp_partial_output in result.output
    assert exp_exit_code == result.exit_code


@pytest.mark.parametrize(
    "flags,exp_result,exp_exit_code",
    (
        (["-i", "-I", "-r" "^method_foo$"], 51.6, 1),
        (["-s", "-p", "-M"], 54.5, 1),
        (["-m", "-f", "45"], 51.4, 0),
    ),
)
def test_run_multiple_flags(flags, exp_result, exp_exit_code, runner):
    """Test CLI with a hodge-podge of flags"""
    cli_inputs = flags + [SAMPLE_DIR]
    result = runner.invoke(cli.main, cli_inputs)

    exp_partial_output = f"actual: {exp_result:.1f}%"
    assert exp_partial_output in result.output
    assert exp_exit_code == result.exit_code


@pytest.mark.parametrize("quiet", (True, False))
def test_generate_badge(quiet, runner, tmp_path):
    """Test expected SVG output when creating a status badge."""
    expected_output_path = os.path.join(FIXTURES, "expected_badge.svg")
    with open(expected_output_path) as f:
        expected_output = f.read()

    expected_output = expected_output.replace("\n", "")

    tmpdir = tmp_path / "testing"
    tmpdir.mkdir()
    expected_path = tmpdir / "interrogate_badge.svg"
    cli_inputs = [
        "--fail-under",
        0,
        "--generate-badge",
        str(tmpdir),
        SAMPLE_DIR,
    ]
    if quiet:
        cli_inputs.append("--quiet")

    result = runner.invoke(cli.main, cli_inputs)
    assert 0 == result.exit_code
    if quiet:
        assert "" == result.output
    else:
        assert str(expected_path) in result.output

    with open(str(expected_path)) as f:
        actual_output = f.read()
        actual_output = actual_output.replace("\n", "")

    assert expected_output == actual_output


def test_incompatible_options_badge_format(runner):
    """Raise an error when mutually exclusive options are used together."""
    result = runner.invoke(cli.main, ["--badge-format", "svg"])
    assert 2 == result.exit_code
    exp_error = (
        "Invalid value: The `--badge-format` option must be used along "
        "with the `-g/--generate-badge option."
    )
    assert exp_error in result.output


def test_incompatible_options_badge_style(runner):
    """Raise an error when mutually exclusive options are used together."""
    result = runner.invoke(cli.main, ["--badge-style", "plastic"])
    assert 2 == result.exit_code
    exp_error = (
        "Invalid value: The `--badge-style` option must be used along "
        "with the `-g/--generate-badge option."
    )
    assert exp_error in result.output
