# Copyright 2020 Lynn Root
"""Collection of general helper functions."""

import contextlib
import itertools
import os
import re
import shutil
import sys

from pathlib import Path

import tabulate


TABLE_SEPARATOR = ["---"]
TERMINAL_WIDTH, _ = shutil.get_terminal_size((80, 20))


def parse_regex(ctx, param, values):
    """Compile a regex if given.

    :param click.Context ctx: click command context.
    :param click.Parameter param: click command parameter (in this case,
        ``ignore_regex`` from ``-r|--ignore-regiex``).
    :param list(str) values: list of regular expressions to be compiled.

    :return: a list of compiled regular expressions.

    .. versionchanged:: 1.1.3 parameter value (``values``) must be a
        ``list`` of ``str``s.
    """
    if not values:
        return
    return [re.compile(v) for v in values]


@contextlib.contextmanager
def smart_open(filename=None, fmode=None):
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


def get_common_base(files):
    """Find the common parent base path for a list of files.

    For example, ``["/usr/src/app", "/usr/src/tests", "/usr/src/app2"]``
    would return ``"/usr/src"``.

    :param files: files to scan.
    :type files: ``iterable``
    :return: Common parent path.
    :rtype: Path
    """


    # Maintain Python 3.5 compatibility
    try:
        common_base =Path(os.path.commonpath(files))
    except TypeError:
        common_base = Path(os.path.commonpath([str(f) for f in files]))
    return common_base


def interrogate_line_formatter(padded_cells, colwidths, colaligns):
    """Format rows of a table to fit terminal.

    :param list(str) padded_cells: row where each cell is padded with
        spacing.
    :param list(int) colwidths: list of widths, by column order.
    :param list(str) colaligns: list of column alignment, by column
        order. Possible values: ``"left"`` or ``"right"``

    :return: a formatted table row
    :rtype: str
    """
    sep, padder = "|", " "
    final_row_width = sum([len(x) for x in padded_cells]) + (
        (len(padded_cells) + 1) * len(sep)
    )
    extra_padding = TERMINAL_WIDTH - final_row_width

    if padded_cells[0].strip() == TABLE_SEPARATOR[0]:
        padder = "-"
        padded_cells = [len(c) * padder for c in padded_cells]

    # Add extra padding to all cells to justify the table to the terminal width.
    padding_per_cell = int(extra_padding / len(padded_cells))

    # If the row width doesn't evenly divide into the cells with equal padding.
    # take the leftover padding and add it to one of the cells.
    final_row_width += len(padded_cells) * padding_per_cell
    remaining_padding = max(0, TERMINAL_WIDTH - final_row_width)
    cell_to_put_extra_padding_into = 0

    to_join = []
    for index, (cell, alignment) in enumerate(zip(padded_cells, colaligns)):
        cell_padding = padding_per_cell
        if index == cell_to_put_extra_padding_into:
            cell_padding += remaining_padding
        if alignment == "right":
            to_append = (padder * cell_padding) + cell
        else:  # default to left
            to_append = cell + (padder * cell_padding)

        to_join.append(to_append)

    ret = sep + sep.join(to_join) + sep
    return ret.rstrip()


InterrogateTableFormat = tabulate.TableFormat(
    lineabove=None,
    linebelowheader=None,
    linebetweenrows=None,
    linebelow=None,
    headerrow=interrogate_line_formatter,
    datarow=interrogate_line_formatter,
    padding=1,
    with_header_hide=None,
)
