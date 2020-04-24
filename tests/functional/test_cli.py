# Copyright 2020 Lynn Root
"""Functional tests for the CLI. I should add more testing..."""
import os

import pytest

from click import testing

from interrogate import cli


HERE = os.path.abspath(os.path.join(os.path.abspath(__file__), os.path.pardir))
SAMPLE_DIR = os.path.join(HERE, "sample")


@pytest.fixture
def runner():
    """Click fixture runner"""
    return testing.CliRunner()


@pytest.mark.parametrize(
    "flags,exp_result,exp_exit_code",
    (
        # no flags
        ([], 46.9, 1),
        # ignore init module
        (["-I"], 46.8, 1),
        # ignore module docs
        (["-M"], 45.5, 1),
        # ignore semiprivate docs
        (["-s"], 47.6, 1),
        # ignore private docs
        (["-p"], 48.8, 1),
        # ignore magic method docs
        (["-m"], 46.7, 1),
        # ignore init method docs
        (["-i"], 45.7, 1),
        # ignore regex
        (["-r", "^method_foo$"], 47.8, 1),
        # exclude file
        (["-e", os.path.join(SAMPLE_DIR, "partial.py")], 53.3, 1),
        # fail under
        (["-f", "40"], 46.9, 0),
    ),
)
def test_run_shortflags(flags, exp_result, exp_exit_code, runner):
    """Test CLI with single short flags"""
    cli_inputs = flags + [SAMPLE_DIR]
    result = runner.invoke(cli.main, cli_inputs)

    exp_partial_output = "actual: {:.1f}%".format(exp_result)
    assert exp_partial_output in result.output
    assert exp_exit_code == result.exit_code


@pytest.mark.parametrize(
    "flags,exp_result,exp_exit_code",
    (
        (["--ignore-init-module"], 46.8, 1),
        (["--ignore-module"], 45.5, 1),
        (["--ignore-semiprivate"], 47.6, 1),
        (["--ignore-private"], 48.8, 1),
        (["--ignore-magic"], 46.7, 1),
        (["--ignore-init-method"], 45.7, 1),
        (["--ignore-regex", "^method_foo$"], 47.8, 1),
        (["--exclude", os.path.join(SAMPLE_DIR, "partial.py")], 53.3, 1),
        (["--fail-under", "40"], 46.9, 0),
    ),
)
def test_run_longflags(flags, exp_result, exp_exit_code, runner):
    """Test CLI with single long flags"""
    cli_inputs = flags + [SAMPLE_DIR]
    result = runner.invoke(cli.main, cli_inputs)

    exp_partial_output = "actual: {:.1f}%".format(exp_result)
    assert exp_partial_output in result.output
    assert exp_exit_code == result.exit_code


@pytest.mark.parametrize(
    "flags,exp_result,exp_exit_code",
    (
        (["-i", "-I", "-r" "^method_foo$"], 46.3, 1),
        (["-s", "-p", "-M"], 48.4, 1),
        (["-m", "-f", "45"], 46.7, 0),
    ),
)
def test_run_multiple_flags(flags, exp_result, exp_exit_code, runner):
    """Test CLI with a hodge-podge of flags"""
    cli_inputs = flags + [SAMPLE_DIR]
    result = runner.invoke(cli.main, cli_inputs)

    exp_partial_output = "actual: {:.1f}%".format(exp_result)
    assert exp_partial_output in result.output
    assert exp_exit_code == result.exit_code
