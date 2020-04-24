# Copyright 2020 Lynn Root
"""
Configuration-related helpers.
Adapted from Black https://github.com/psf/black/blob/master/black.py
"""

import pathlib

import attr
import click
import toml


@attr.s
class InterrogateConfig:
    """Configuration related to interrogating."""

    fail_under = attr.ib(default=80.0)
    ignore_regex = attr.ib(default=False)
    ignore_magic = attr.ib(default=False)
    ignore_module = attr.ib(default=False)
    ignore_private = attr.ib(default=False)
    ignore_semiprivate = attr.ib(default=False)
    ignore_init_method = attr.ib(default=False)
    ignore_init_module = attr.ib(default=False)


def find_project_root(srcs):
    """Return a directory containing .git, .hg, or pyproject.toml.
    That directory can be one of the directories passed in `srcs` or their
    common parent.
    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.k
    """
    if not srcs:
        return pathlib.Path("/").resolve()

    common_base = min(pathlib.Path(src).resolve() for src in srcs)
    if common_base.is_dir():
        # Append a fake file so `parents` below returns `common_base_dir`, too.
        common_base /= "fake-file"
    for directory in common_base.parents:
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory


def find_pyproject_toml(path_search_start):
    """Find the absolute filepath to a pyproject.toml if it exists."""
    project_root = find_project_root(path_search_start)
    pyproject_toml = project_root / "pyproject.toml"
    return str(pyproject_toml) if pyproject_toml.is_file() else None


def parse_pyproject_toml(path_config):
    """Parse a pyproject toml file and return relevant parts for Interrogate."""
    pyproject_toml = toml.load(path_config)
    config = pyproject_toml.get("tool", {}).get("interrogate", {})
    return {
        k.replace("--", "").replace("-", "_"): v for k, v in config.items()
    }


def read_pyproject_toml(ctx, param, value):
    """Inject conf from "pyproject.toml" into Click's `ctx`.

    These override option defaults, but still respect option values
    provided via the CLI.
    """
    assert not isinstance(value, (int, bool)), "Invalid parameter type passed"
    if not value:
        value = find_pyproject_toml(ctx.params.get("src", ()))
        if value is None:
            return None

    try:
        config = parse_pyproject_toml(value)
    except (toml.TomlDecodeError, OSError) as e:
        raise click.FileError(
            filename=value,
            hint="Error reading configuration file: {}".format(e),
        )

    if not config:
        return None

    if ctx.default_map is None:
        ctx.default_map = {}

    ctx.default_map.update(config)
    return value
