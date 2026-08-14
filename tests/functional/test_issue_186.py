"""Tests for issue #186: --fail-under=100 with missing docstrings."""

import os

import pytest

from interrogate import config, coverage


def _write_module(path, n_funcs, n_missing):
    """Write a module with ``n_funcs`` functions, ``n_missing`` undocumented."""
    lines = ['"""Module docstring."""\n']
    for i in range(n_funcs):
        lines.append(f"def f{i}():\n")
        if i >= n_missing:
            lines.append(f'    """Doc {i}."""\n')
        lines.append("    pass\n\n")
    with open(path, "w") as f:
        f.write("".join(lines))


@pytest.mark.parametrize(
    "n_funcs,n_missing,exp_ret",
    [
        (1999, 1, 1),  # 1999/2000 = 99.95% -> round(.,1) == 100.0
        (1999, 0, 0),  # genuinely complete
        (10, 1, 1),  # small codebase, already worked before
    ],
)
def test_fail_under_100_with_missing_docstring(
    tmp_path, n_funcs, n_missing, exp_ret
):
    """--fail-under=100 must fail whenever any docstring is missing."""
    mod = os.path.join(str(tmp_path), "mod.py")
    _write_module(mod, n_funcs, n_missing)
    conf = config.InterrogateConfig(fail_under=100)
    cov = coverage.InterrogateCoverage(paths=[mod], conf=conf)
    results = cov.get_coverage()
    assert n_missing == results.missing
    assert (
        exp_ret == results.ret_code
    ), "missing={} total={} perc={} ret={}".format(
        results.missing, results.total, results.perc_covered, results.ret_code
    )
