# Copyright 2020 Lynn Root
"""
Configuration-related helpers.
"""
# Adapted from Black https://github.com/psf/black/blob/master/black.py.

import pathlib

import attr
import click
import toml


@attr.s
class InterrogateConfig:
    """Configuration related to interrogating a given codebase.

    :param fail_under: Fail when coverage % is less than a given amount.
    :type fail_under: `int` or `float`
    :param str ignore_regex: Regex identifying class, method, and
        function names to ignore.
    :param bool ignore_magic: Ignore all magic methods of classes.
    :param bool ignore_module: Ignore module-level docstrings.
    :param bool ignore_private: Ignore private classes, methods, and
        functions starting with two underscores.
    :param bool ignore_semiprivate: Ignore semiprivate classes, methods,
        and functions starting with a single underscore.
    :param bool ignore_init_method: Ignore ``__init__`` method of
        classes.
    :param bool ignore_init_module: Ignore ``__init__.py`` modules.
    """

    fail_under = attr.ib(default=80.0)
    ignore_regex = attr.ib(default=False)
    ignore_magic = attr.ib(default=False)
    ignore_module = attr.ib(default=False)
    ignore_private = attr.ib(default=False)
    ignore_semiprivate = attr.ib(default=False)
    ignore_init_method = attr.ib(default=False)
    ignore_init_module = attr.ib(default=False)
    include_regex = attr.ib(default=False)


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
    """Parse ``pyproject.toml`` file and return relevant parts for Interrogate.

    :param str path_config: Path to ``pyproject.toml`` file.
    :return: Dictionary representing configuration for Interrogate.
    :rtype: dict
    :raise OSError: an I/O-related error when opening ``pyproject.toml``.
    :raise toml.TomlDecodeError: unable to load ``pyproject.toml``.
    """
    pyproject_toml = toml.load(path_config)
    config = pyproject_toml.get("tool", {}).get("interrogate", {})
    return {
        k.replace("--", "").replace("-", "_"): v for k, v in config.items()
    }


def read_pyproject_toml(ctx, param, value):
    """Inject configuration from ``pyproject.toml`` into ``ctx``.

    These override option defaults, but still respect option values
    provided via the CLI.

    :param click.Context ctx: click command context.
    :param click.Parameter param: click command parameter (in this case,
        ``config`` from ``-c|--config``).
    :param str value: path to ``pyproject.toml`` file.

    :return: path to ``pyproject.toml`` file.
    :rtype: str

    :raise click.FileError: if ``pyproject.toml`` is not parseable or
        otherwise not available (i.e. does not exist).
    """
    assert not isinstance(value, (int, bool)), "Invalid parameter type passed"
    if not value:
        value = find_pyproject_toml(ctx.params.get("paths", ()))
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

    # for backwards compatibility. before 1.1.3, only one regex was allowed.
    # with 1.1.3+, multiple regexes can be provided, but we want to honor
    # those that configured their pyproject.toml to be a single regex
    # string (since now we're expecting a list of strings).
    if "ignore_regex" in config:
        if isinstance(config["ignore_regex"], str):
            config["ignore_regex"] = [config["ignore_regex"]]

    ctx.default_map.update(config)
    return value
