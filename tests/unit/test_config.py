# Copyright 2020 Lynn Root
"""Unit tests for interrogate/config.py module"""

import configparser
import pathlib

import click
import pytest


try:
    import tomllib
except ImportError:
    import tomli as tomllib

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
    with monkeypatch.context() as mp:
        expected = pathlib.Path(expected)
        if patch_func:
            mp.setattr(config.pathlib.Path, patch_func, lambda x: True)
        mp.setattr(config.pathlib.Path, "resolve", lambda x: x)

        actual = config.find_project_root(srcs)

        assert expected == actual


@pytest.mark.parametrize(
    "is_file,expected",
    (
        (True, str(pathlib.Path("/usr/src/pyproject.toml"))),
        (False, None),
    ),
)
def test_find_project_config(is_file, expected, mocker, monkeypatch):
    """Return absolute path if pyproject.toml or setup.cfg is detected."""
    with monkeypatch.context() as mp:
        mp.setattr(config.pathlib.Path, "is_file", lambda x: is_file)
        mp.setattr(config.pathlib.Path, "resolve", lambda x: x)

        actual = config.find_project_config(("/usr/src/app",))
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


@pytest.mark.parametrize(
    "value,exp_value",
    (
        (None, []),
        ("", []),
        ("[]", []),
        ("[foo,bar,baz]", ["foo", "bar", "baz"]),
        ('["foo","bar","baz"]', ["foo", "bar", "baz"]),
        ('["foo", "bar", "baz"]', ["foo", "bar", "baz"]),
        ('"foo", "bar", "baz"', ["foo", "bar", "baz"]),
        (
            '"^get$", "^mock_.*", ".*BaseClass.*"',
            ["^get$", "^mock_.*", ".*BaseClass.*"],
        ),
        (
            "^get$,^mock_.*,.*BaseClass.*",
            ["^get$", "^mock_.*", ".*BaseClass.*"],
        ),
    ),
)
def test_sanitize_list_values(value, exp_value):
    """Return expected list from a string that should be a list."""
    assert exp_value == config.sanitize_list_values(value)


def test_parse_setup_cfg(tmpdir):
    """Return expected config data from a setup.cfg file."""
    cfg_data = (
        "[tool:foo]\n"
        'foo = "bar"\n'
        "[tool:interrogate]\n"
        "ignore-init-module = true\n"
        "ignore-init-method = false\n"
        "exclude = foo/bar,baz\n"
        "output = foo.txt\n"
    )

    p = tmpdir.mkdir("interrogate-testing").join("setup.cfg")
    p.write(cfg_data)

    actual = config.parse_setup_cfg(str(p))
    expected = {
        "ignore_init_module": True,
        "ignore_init_method": False,
        "exclude": ["foo/bar", "baz"],
        "output": "foo.txt",
    }
    assert expected == actual


def test_parse_setup_cfg_raises(tmpdir):
    """Return nothing if no interrogate section was found."""
    cfg_data = "[tool.foo]\n" 'foo = "bar"\n'

    p = tmpdir.mkdir("interrogate-testing").join("setup.cfg")
    p.write(cfg_data)

    actual = config.parse_setup_cfg(str(p))
    assert actual is None


def test_read_config_file_none(mocker, monkeypatch):
    """Return nothing if no pyproject.toml or setup.cfg is found."""
    monkeypatch.setattr(config, "find_project_config", lambda x: None)
    ctx = mocker.Mock()
    actual = config.read_config_file(ctx, "config", None)
    assert actual is None


@pytest.mark.parametrize(
    "value,ret_config,default_map,exp_ret,exp_defaults",
    (
        (None, None, None, None, None),
        (
            "pyproject.toml",
            {"fail_under": 90},
            None,
            "pyproject.toml",
            {"fail_under": 90},
        ),
        (
            "setup.cfg",
            {"fail_under": 90},
            None,
            "setup.cfg",
            {"fail_under": 90},
        ),
        ("setup.cfg", {"fail_under": 90}, {}, "setup.cfg", {"fail_under": 90}),
        (
            "pyproject.toml",
            {"fail_under": 90},
            {"foo": "bar"},
            "pyproject.toml",
            {"fail_under": 90, "foo": "bar"},
        ),
        (
            "setup.cfg",
            {"fail_under": 90},
            {"foo": "bar"},
            "setup.cfg",
            {"fail_under": 90, "foo": "bar"},
        ),
        # test backwards config for turning a single regex str (<1.1.3)
        # to a list of regex strs (>=1.1.3)
        (
            "pyproject.toml",
            {"ignore_regex": "^get_.*"},
            None,
            "pyproject.toml",
            {"ignore_regex": ["^get_.*"]},
        ),
        (
            "pyproject.toml",
            {"ignore_regex": ["^get_.*", "^post_.*"]},
            None,
            "pyproject.toml",
            {"ignore_regex": ["^get_.*", "^post_.*"]},
        ),
    ),
)
def test_read_config_file(
    value, ret_config, default_map, exp_ret, exp_defaults, mocker, monkeypatch
):
    """Parse config from a given pyproject.toml or setup.cfg file."""
    monkeypatch.setattr(config, "find_project_config", lambda x: value)
    monkeypatch.setattr(config, "parse_pyproject_toml", lambda x: ret_config)
    monkeypatch.setattr(config, "parse_setup_cfg", lambda x: ret_config)
    ctx = mocker.Mock(default_map=default_map, params={})

    actual = config.read_config_file(ctx, "config", value)
    assert exp_ret == actual
    assert exp_defaults == ctx.default_map


def test_read_config_file_raises(mocker, monkeypatch):
    """Handle exceptions while reading pyproject.toml/setup.cfg, if any."""
    toml_error = tomllib.TOMLDecodeError("toml error")
    os_error = OSError("os error")
    mock_parse_pyproject_toml = mocker.Mock()
    mock_parse_pyproject_toml.side_effect = (toml_error, os_error)
    monkeypatch.setattr(
        config, "parse_pyproject_toml", mock_parse_pyproject_toml
    )
    cfg_error = configparser.ParsingError("cfg parsing error")
    mock_parse_setup_cfg = mocker.Mock()
    mock_parse_setup_cfg.side_effect = (cfg_error,)
    monkeypatch.setattr(config, "parse_setup_cfg", mock_parse_setup_cfg)

    error_msg = "Error reading configuration file: toml error"
    with pytest.raises(click.FileError, match=error_msg):
        config.read_config_file({}, "foo", "pyproject.toml")

    error_msg = "Error reading configuration file: os error"
    with pytest.raises(click.FileError, match=error_msg):
        config.read_config_file({}, "foo", "pyproject.toml")

    error_msg = (
        "Error reading configuration file: Source contains parsing errors: "
        "'cfg parsing error'"
    )
    with pytest.raises(click.FileError, match=error_msg):
        config.read_config_file({}, "foo", "setup.cfg")
