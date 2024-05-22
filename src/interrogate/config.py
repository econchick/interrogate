# Copyright 2020-2024 Lynn Root
"""
Configuration-related helpers.
"""
# Adapted from Black https://github.com/psf/black/blob/master/black.py.

from __future__ import annotations

import configparser
import re

from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

import attr
import click

if TYPE_CHECKING:
    from os import PathLike

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


# TODO: idea: break out InterrogateConfig into two classes: one for
# running the tool, one for reporting the results
@attr.s
class InterrogateConfig:
    """Configuration related to interrogating a given codebase.

    :param bool color: Highlight verbose output with color.
    :param str docstring_style: Style of docstrings to follow. Choices:
        "sphinx" (default), "google".
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
    :param bool ignore_nested_functions: Ignore nested functions and
        methods.
    :param bool ignore_init_module: Ignore ``__init__.py`` modules.
    :param str include_regex: Regex identifying class, method, and
        function names to include.
    :param bool omit_covered_files: Omit reporting files that have 100%
        documentation coverage.
    :param bool ignore_overloaded_functions: Ignore `@typing.overload`-decorated
        functions.
    """

    VALID_STYLES = ("sphinx", "google")

    color: bool = attr.ib(default=False)
    docstring_style: str = attr.ib(default="sphinx")
    fail_under: float = attr.ib(default=80.0)
    ignore_regex: list[re.Pattern[str]] | None = attr.ib(default=None)
    ignore_magic: bool = attr.ib(default=False)
    ignore_module: bool = attr.ib(default=False)
    ignore_private: bool = attr.ib(default=False)
    ignore_semiprivate: bool = attr.ib(default=False)
    ignore_init_method: bool = attr.ib(default=False)
    ignore_init_module: bool = attr.ib(default=False)
    ignore_nested_classes: bool = attr.ib(default=False)
    ignore_nested_functions: bool = attr.ib(default=False)
    ignore_property_setters: bool = attr.ib(default=False)
    ignore_property_decorators: bool = attr.ib(default=False)
    ignore_overloaded_functions: bool = attr.ib(default=False)
    include_regex: list[re.Pattern[str]] | None = attr.ib(default=None)
    omit_covered_files: bool = attr.ib(default=False)

    @docstring_style.validator
    def _check_style(self, attribute: str, value: str) -> None:
        """Validate selected choice for docstring style"""
        if value not in self.VALID_STYLES:
            raise ValueError(
                f"Invalid `docstring_style` '{value}'. Valid values: "
                f"{', '.join(self.VALID_STYLES)}"
            )


def find_project_root(srcs: Sequence[PathLike[str] | str]) -> Path:
    """Return a directory containing .git, .hg, or pyproject.toml.
    That directory can be one of the directories passed in `srcs` or their
    common parent.
    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not srcs:
        return Path("/").resolve()

    common_base = min(Path(src).resolve() for src in srcs)
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


def find_project_config(path_search_start: Sequence[PathLike[str] | str]) -> str | None:
    """Find the absolute filepath to a pyproject.toml if it exists."""
    project_root = find_project_root(path_search_start)
    pyproject_toml = project_root / "pyproject.toml"
    if pyproject_toml.is_file():
        return str(pyproject_toml)

    setup_cfg = project_root / "setup.cfg"
    return str(setup_cfg) if setup_cfg.is_file() else None


def parse_pyproject_toml(path_config: PathLike[str] | str) -> dict[str, Any]:
    """Parse ``pyproject.toml`` file and return relevant parts for Interrogate.

    :param str path_config: Path to ``pyproject.toml`` file.
    :return: Dictionary representing configuration for Interrogate.
    :rtype: dict
    :raise OSError: an I/O-related error when opening ``pyproject.toml``.
    :raise tomllib.TOMLDecodeError: unable to load ``pyproject.toml``.
    """
    pyproject_toml = tomllib.loads(Path(path_config).read_text())
    config = pyproject_toml.get("tool", {}).get("interrogate", {})
    return {
        k.replace("--", "").replace("-", "_"): v for k, v in config.items()
    }


def sanitize_list_values(value: str) -> list[str | None]:
    """Parse a string of list items to a Python list.

    This is super hacky...

    :param str value: string-representation of a Python list
    :return: List of strings
    :rtype: list
    """
    if not value:
        return []

    if value.startswith("["):
        value = value[1:]
    if value.endswith("]"):
        value = value[:-1]
    if not value:
        return []

    raw_values = [v.strip() for v in value.split(",")]
    return [v.strip('"') for v in raw_values]


def parse_setup_cfg(path_config: str) -> dict[str, Any] | None:
    """Parse ``setup.cfg`` file and return relevant parts for Interrogate.

    This is super hacky...

    :param str path_config: Path to ``setup.cfg`` file.
    :return: Dictionary representing configuration for Interrogate.
    :rtype: dict
    :raise OSError: an I/O-related error when opening ``setup.cfg``.
    :raise configparser.ConfigParser: unable to load ``setup.cfg``.
    """
    cfg = configparser.ConfigParser()
    cfg.read(path_config)

    try:
        interrogate_section = cfg["tool:interrogate"]
    except KeyError:
        return None

    keys_for_list_values = ["whitelist_regex", "ignore_regex", "exclude"]
    raw_config = dict(interrogate_section.items())
    config = {
        k.replace("--", "").replace("-", "_"): v for k, v in raw_config.items()
    }
    for k, v in config.items():
        if k in keys_for_list_values:
            config[k] = sanitize_list_values(v)  # type: ignore
        elif v.lower() == "false":
            config[k] = False  # type: ignore
        elif v.lower() == "true":
            config[k] = True  # type: ignore
    return config


def read_config_file(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    """Inject config from ``pyproject.toml`` or ``setup.py`` into ``ctx``.

    These override option defaults, but still respect option values
    provided via the CLI.

    :param click.Context ctx: click command context.
    :param click.Parameter param: click command parameter (in this case,
        ``config`` from ``-c|--config``).
    :param str value: path to ``pyproject.toml`` or ``setup.cfg`` file.

    :return: path to ``pyproject.toml`` or ``setup.cfg`` file.
    :rtype: str

    :raise click.FileError: if ``pyproject.toml`` or ``setup.cfg`` is not
        parseable or otherwise not available (i.e. does not exist).
    """
    if not value:
        paths = ctx.params.get("paths")
        if not paths:
            paths = (Path.cwd(),)
        value = find_project_config(paths)
        if value is None:
            return None

    config = None
    if value.endswith(".toml"):
        try:
            config = parse_pyproject_toml(value)
        except (tomllib.TOMLDecodeError, OSError) as e:
            raise click.FileError(
                filename=value,
                hint=f"Error reading configuration file: {e}",
            )

    elif value.endswith(".cfg"):
        try:
            config = parse_setup_cfg(value)
        except configparser.ParsingError as e:
            raise click.FileError(
                filename=value,
                hint=f"Error reading configuration file: {e}",
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
