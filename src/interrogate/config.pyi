import pathlib

from typing import Any, Dict, Iterable, Optional, Pattern, Union

import click


class InterrogateConfig:
    fail_under: float
    ignore_regex: Union[Iterable[Pattern], bool]
    ignore_magic: bool
    ignore_module: bool
    ignore_private: bool
    ignore_semiprivate: bool
    ignore_init_method: bool
    ignore_init_module: bool
    include_regex: Union[Iterable[Pattern], bool]


def find_project_root(srcs: Iterable[str]) -> pathlib.PosixPath: ...


def find_pyproject_toml(path_search_start: str) -> Optional[str]: ...


def parse_pyproject_toml(path_config: str) -> Dict[str, Any]: ...


def read_pyproject_toml(ctx: click.Context, param: click.Parameter, value: Union[str, int, bool, None]) -> Optional[str]: ...
