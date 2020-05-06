from io import TextIOWrapper
from typing import (
    Iterator,
    List,
    Optional,
    Pattern,
    Tuple,
    Union,
)

import click


TABLE_SEPARATOR: List[bool]
TERMINAL_WIDTH: int


def parse_regex(ctx: click.Context, param: click.Parameter, values: Union[Tuple[str], None]) -> Optional[Iterator[Pattern]]: ...


def smart_open(filename: Optional[str] = ..., fmode: Optional[str] = ...) -> Iterator[TextIOWrapper]: ...


def get_common_base(files: List[str]) -> str: ...


def interrogate_line_formatter(padded_cells: List[str], colwidths: List[int], colaligns: List[str]) -> str: ...
