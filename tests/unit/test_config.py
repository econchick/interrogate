# Copyright 2020 Lynn Root
"""Unit tests for interrogate/config.py module"""

import pathlib

import click
import pytest
import toml

from interrogate import config


@pytest.mark.parametrize(
    "srcs,patch_func, expected",
    (
        # return root dir
        ((), None, "/"),
        # return directory with .git
        (("/usr/src/app", "/usr/src/tests"), "exists", "/usr/src"),
        # return directory with .hg
        (("/usr/src/app", "/usr/src/tests"), "is_dir", "/usr/src/app"),
        # return directory with pyproject.toml
        (("/usr/src/app/pyproject.toml",), "is_file", "/usr/src/app"),
        # return root if nothing matches
        (("/usr/src/app", "/usr/src/test"), None, "/"),
    ),
)
def test_find_project_root(srcs, patch_func, expected, monkeypatch):
    """Return expected directory of project root."""
    expected = pathlib.Path(expected)
    if patch_func:
        monkeypatch.setattr(config.pathlib.Path, patch_func, lambda x: True)
    monkeypatch.setattr(config.pathlib.Path, "resolve", lambda x: x)

    actual = config.find_project_root(srcs)

    assert expected == actual


@pytest.mark.parametrize(
    "is_file,expected",
    ((True, str(pathlib.Path("/usr/src/pyproject.toml"))), (False, None)),
)
def test_find_pyproject_toml(is_file, expected, mocker, monkeypatch):
    """Return absolute path if pyproject.toml is detected."""
    monkeypatch.setattr(config.pathlib.Path, "is_file", lambda x: is_file)
    monkeypatch.setattr(config.pathlib.Path, "resolve", lambda x: x)

    actual = config.find_pyproject_toml(("/usr/src/app",))
    assert expected == actual


def test_parse_pyproject_toml(tmpdir):
    """Return expected config data from a pyproject.toml file."""
    toml_data = (
        "[tool.foo]\n"
        'foo = "bar"\n'
        "[tool.interrogate]\n"
        "ignore-init-module = true\n"
    )

    p = tmpdir.mkdir("interrogate-testing").join("pyproject.toml")
    p.write(toml_data)

    actual = config.parse_pyproject_toml(str(p))
    assert {"ignore_init_module": True} == actual


def test_read_pyproject_toml_none(mocker, monkeypatch):
    """Return nothing if no pyproject.toml is found."""
    monkeypatch.setattr(config, "find_pyproject_toml", lambda x: None)
    ctx = mocker.Mock()
    actual = config.read_pyproject_toml(ctx, "config", None)
    assert actual is None


@pytest.mark.parametrize(
    "value,ret_config,default_map,exp_ret,exp_defaults",
    (
        (None, None, None, None, None),
        ("a-value", {"fail_under": 90}, None, "a-value", {"fail_under": 90}),
        ("a-value", {"fail_under": 90}, {}, "a-value", {"fail_under": 90}),
        (
            "a-value",
            {"fail_under": 90},
            {"foo": "bar"},
            "a-value",
            {"fail_under": 90, "foo": "bar"},
        ),
        # test backwards config for turning a single regex str (<1.1.3)
        # to a list of regex strs (>=1.1.3)
        (
            "a-value",
            {"ignore_regex": "^get_.*"},
            None,
            "a-value",
            {"ignore_regex": ["^get_.*"]},
        ),
        (
            "a-value",
            {"ignore_regex": ["^get_.*", "^post_.*"]},
            None,
            "a-value",
            {"ignore_regex": ["^get_.*", "^post_.*"]},
        ),
    ),
)
def test_read_pyproject_toml(
    value, ret_config, default_map, exp_ret, exp_defaults, mocker, monkeypatch
):
    """Parse config from a given pyproject.toml file."""
    monkeypatch.setattr(
        config, "find_pyproject_toml", lambda x: "pyproject.toml"
    )
    monkeypatch.setattr(config, "parse_pyproject_toml", lambda x: ret_config)
    ctx = mocker.Mock(default_map=default_map, params={})

    actual = config.read_pyproject_toml(ctx, "config", value)
    assert exp_ret == actual
    assert exp_defaults == ctx.default_map


def test_read_pyproject_toml_raises(mocker, monkeypatch):
    """Handle expected exceptions while reading pyproject.toml, if any."""
    with pytest.raises(AssertionError, match="Invalid parameter type passed"):
        config.read_pyproject_toml({}, "foo", True)

    with pytest.raises(AssertionError, match="Invalid parameter type passed"):
        config.read_pyproject_toml({}, "foo", 123)

    toml_error = toml.TomlDecodeError("toml error", doc="foo", pos=0)
    os_error = OSError("os error")
    mock_parse_pyproject_toml = mocker.Mock()
    mock_parse_pyproject_toml.side_effect = (toml_error, os_error)
    monkeypatch.setattr(
        config, "parse_pyproject_toml", mock_parse_pyproject_toml
    )

    error_msg = "Error reading configuration file: toml error"
    with pytest.raises(click.FileError, match=error_msg):
        config.read_pyproject_toml({}, "foo", "bar")

    error_msg = "Error reading configuration file: os error"
    with pytest.raises(click.FileError, match=error_msg):
        config.read_pyproject_toml({}, "foo", "bar")
