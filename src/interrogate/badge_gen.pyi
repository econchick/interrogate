from typing import Dict, List, Tuple

from interrogate.coverage import InterrogateResults


DEFAULT_FILENAME: str
COLORS: Dict[str, str]
COLOR_RANGES: List[Tuple[int, str]]


def save_badge(badge: str, output: str) -> str: ...


def get_badge(result: float, color: str) -> str: ...


def get_color(result: float) -> str: ...


def create(output: str, result: InterrogateResults) -> str: ...
