"""Tests for issue #104: how an explicitly-named file is judged."""

import os

import pytest

from interrogate import coverage


SRC = '"""M."""\n\n\ndef f():\n    pass\n'


def _cov(tmp_path, name, extensions=(), content=SRC, direct=True):
    """Build a coverage object over a freshly written file."""
    p = os.path.join(str(tmp_path), name)
    with open(p, "w") as f:
        f.write(content)
    target = p if direct else str(tmp_path)
    return coverage.InterrogateCoverage(paths=[target], extensions=extensions)


def test_ext_option_honoured_for_explicit_file(tmp_path):
    """--ext must work for an explicitly named file, as it does for a dir."""
    cov = _cov(tmp_path, "a.ipynb", extensions=("ipynb",))
    assert [
        os.path.join(str(tmp_path), "a.ipynb")
    ] == cov.get_filenames_from_paths()


def test_ext_option_dir_walk_control(tmp_path):
    """Control: the same file found via directory walk is accepted."""
    cov = _cov(tmp_path, "a.ipynb", extensions=("ipynb",), direct=False)
    assert [
        os.path.join(str(tmp_path), "a.ipynb")
    ] == cov.get_filenames_from_paths()


def test_executable_python_script_without_py_suffix(tmp_path):
    """A #!-python script without .py should be interrogated (issue #104)."""
    content = "#!/usr/bin/env python\n" + SRC
    cov = _cov(tmp_path, "postgres-ready", content=content)
    assert [
        os.path.join(str(tmp_path), "postgres-ready")
    ] == cov.get_filenames_from_paths()


def test_non_python_extensionless_file_still_rejected(tmp_path):
    """Control: a file with no shebang and no extension is still rejected."""
    cov = _cov(tmp_path, "README", content="not python\n")
    with pytest.raises(SystemExit):
        cov.get_filenames_from_paths()
