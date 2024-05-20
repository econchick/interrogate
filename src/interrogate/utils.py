# Copyright 2020-2024 Lynn Root
"""Collection of general helper functions."""

from __future__ import annotations

import contextlib
import functools
import os
import pathlib
import re
import shutil
import sys

from typing import IO, Any, Final, Iterator, Sequence

import colorama
import tabulate

from click import Context, Parameter
from py import io as py_io

from interrogate.config import InterrogateConfig


IS_WINDOWS: Final[bool] = sys.platform == "win32"


def parse_regex(
    ctx: Context, param: Parameter, values: list[str]
) -> list[re.Pattern[str]] | None:
    """Compile a regex if given.

    :param click.Context ctx: click command context.
    :param click.Parameter param: click command parameter (in this case,
        ``ignore_regex`` from ``-r|--ignore-regex``).
    :param list(str) values: list of regular expressions to be compiled.

    :return: a list of compiled regular expressions.

    .. versionchanged:: 1.1.3 parameter value (``values``) must be a
        ``list`` of ``str``s.
    """
    if not values:
        return None
    return [re.compile(v) for v in values]


@contextlib.contextmanager
def smart_open(
    filename: str | None = None, fmode: str = "w"
) -> Iterator[IO[Any]]:
    """Context manager to handle both stdout & files in the same manner.

    :param filename: Filename to open.
    :type filename: ``str`` or ``None``
    :param fmode: Mode in which to open a given file.
    :type fmode: ``str`` or ``None``
    """
    if filename and filename != "-":
        fh = open(filename, fmode)
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def get_common_base(files: Sequence[str | pathlib.Path]) -> str:
    """Find the common parent base path for a list of files.

    For example, ``["/usr/src/app", "/usr/src/tests", "/usr/src/app2"]``
    would return ``"/usr/src"``.

    :param files: files to scan.
    :type files: ``iterable``
    :return: Common parent path.
    :rtype: str
    """
    commonbase = pathlib.Path(os.path.commonprefix(files))
    # commonprefix may return an invalid path, e.g. for "/usr/foobar"
    # and "/usr/foobaz", it will return "/usr/fooba", so we'll need to
    # find its parent directory if that's the case.
    while not commonbase.exists():
        commonbase = commonbase.parent
    return str(commonbase)


class OutputFormatter:
    """Interrogate results formatter."""

    TERMINAL_WIDTH, _ = shutil.get_terminal_size((80, 20))
    TABLE_SEPARATOR = ["---"]

    def __init__(self, config: InterrogateConfig, file: IO[Any] | None = None):
        self.config = config
        self.tw = py_io.TerminalWriter(file=file)

    def should_markup(self) -> bool:
        """Return whether or not color markup should be added to output."""
        if self.config.color is False:
            return False

        # click should handle this already, but just being safe
        if os.environ.get("INTERROGATE_COLOR", "").lower() in ("0", "false"):
            return False

        # this will do some extra checks (java + nt runtime, is atty, etc)
        if not self.tw.hasmarkup:
            return False

        return True

    def set_detailed_markup(self, padded_cells: list[str]) -> list[str]:
        """Add markup specific to the detailed output section."""
        if not self.should_markup():
            return padded_cells

        markup = None
        status = padded_cells[-1]
        if "MISSED" in status:
            # markup = 31  # red foreground
            markup = colorama.Fore.RED
        elif "COVERED" in status:
            # markup = 32  # green foreground
            markup = colorama.Fore.GREEN

        if markup is None:
            return padded_cells

        marked_up_padded_cells = []
        for cell in padded_cells:
            cell = markup + cell + colorama.Style.RESET_ALL
            marked_up_padded_cells.append(cell)

        return marked_up_padded_cells

    def set_summary_markup(self, padded_cells: list[str]) -> list[str]:
        """Add markup specific to the summary output section."""
        if not self.should_markup():
            return padded_cells

        # sanity check
        if len(padded_cells) != 5:
            return padded_cells

        cover_perc = padded_cells[-1].strip().strip("%")
        try:
            cover_perc_fl = float(cover_perc)
        except (ValueError, TypeError):
            return padded_cells

        markup = None

        if cover_perc_fl < self.config.fail_under:
            markup = colorama.Fore.RED
        else:
            markup = colorama.Fore.GREEN

        marked_up_padded_cells = []
        for cell in padded_cells:
            cell = markup + cell + colorama.Style.RESET_ALL
            marked_up_padded_cells.append(cell)

        return marked_up_padded_cells

    def _interrogate_line_formatter(
        self,
        padded_cells: list[str],
        colwidths: list[int],
        colaligns: list[str],
        table_type: str,
    ) -> str:
        """Format rows of a table to fit terminal.

        :param list(str) padded_cells: row where each cell is padded with
            spacing.
        :param list(int) colwidths: list of widths, by column order.
        :param list(str) colaligns: list of column alignment, by column
            order. Possible values: ``"left"`` or ``"right"``
        :param str table_type: Table type of either "detailed" (second
            level of output verbosity), or "summary" (first level of
            output verbosity).

        :return: a formatted table row
        :rtype: str
        """
        sep, padder = "|", " "
        final_row_width = sum([len(x) for x in padded_cells]) + (
            (len(padded_cells) + 1) * len(sep)
        )
        if IS_WINDOWS:
            # windows may pad the output a bit unknowingly (see
            # https://github.com/econchick/interrogate/issues/20)
            final_row_width += 1
        extra_padding = max(self.TERMINAL_WIDTH - final_row_width, 0)

        if padded_cells[0].strip() == self.TABLE_SEPARATOR[0]:
            padder = "-"
            padded_cells = [len(c) * padder for c in padded_cells]

        # Add extra padding to all cells to justify the table to the
        # terminal width.
        padding_per_cell = int(extra_padding / len(padded_cells))

        # If the row width doesn't evenly divide into the cells with
        # equal padding; take the leftover padding and add it to one
        # of the cells.
        final_row_width += len(padded_cells) * padding_per_cell
        remaining_padding = max(0, self.TERMINAL_WIDTH - final_row_width)
        cell_to_put_extra_padding_into = 0

        if table_type == "detailed":
            padded_cells = self.set_detailed_markup(padded_cells)
        elif table_type == "summary":
            padded_cells = self.set_summary_markup(padded_cells)

        to_join = []
        for index, (cell, alignment) in enumerate(
            zip(padded_cells, colaligns)
        ):
            cell_padding = padding_per_cell

            if index == cell_to_put_extra_padding_into:
                cell_padding += remaining_padding
            if alignment == "right":
                to_append = (padder * cell_padding) + cell
            elif alignment == "center":
                left_padding = cell_padding // 2
                right_padding = cell_padding - left_padding
                to_append = (
                    (padder * left_padding) + cell + (padder * right_padding)
                )
            else:  # default to left
                to_append = cell + (padder * cell_padding)

            to_join.append(to_append)

        ret = sep + sep.join(to_join) + sep
        return ret.rstrip()

    def get_table_formatter(self, table_type: str) -> tabulate.TableFormat:
        """Get a `tabulate` table formatter.

        :param str table_type: Table type of either "detailed" (second
            level of output verbosity), or "summary" (first level of
            output verbosity).

        :return: A table formatter for printing desired output.
        :rtype: tabulate.TableFormat
        """
        assert table_type in (
            "detailed",
            "summary",
        ), f"'{table_type}' is not a supported table type"
        line_formatter = functools.partial(
            self._interrogate_line_formatter, table_type=table_type
        )
        return tabulate.TableFormat(
            lineabove=None,
            linebelowheader=None,
            linebetweenrows=None,
            linebelow=None,
            headerrow=line_formatter,
            datarow=line_formatter,
            padding=1,
            with_header_hide=None,
        )
