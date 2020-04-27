# Copyright 2020 Lynn Root
"""Collection of general helper functions."""

import contextlib
import itertools
import re
import shutil
import sys

import tabulate


TABLE_SEPARATOR = ["---"]
TERMINAL_WIDTH, _ = shutil.get_terminal_size((80, 20))


def parse_regex(ctx, param, value):
    """Compile a regex if given.

    :param click.Context ctx: click command context.
    :param click.Parameter param: click command parameter (in this case,
        ``ignore_regex`` from ``-r|--ignore-regiex``).
    :param str value: regular expression to be compiled.

    :return: a compiled regular expression.
    """
    if value is None:
        return
    return re.compile(value)


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
    :rtype: str
    """

    def allnamesequal(name):
        """Return if all names in an iterable are equal."""
        return all(n == name[0] for n in name[1:])

    level_slices = zip(*[f.split("/") for f in files])
    tw = itertools.takewhile(allnamesequal, level_slices)
    return "/".join(x[0] for x in tw)


def interrogate_line_formatter(padded_cells, colwidths, colaligns):
    """Format rows of a table to fit terminal.

    :param list(str) padded_cells: row where each cell is padded with spacing.
    :param list(int) colwidths: list of widths, by column order.
    :param list(str) colaligns: list of column alignment, by column order.

    :return: a formatted table row
    :rtype: str
    """
    sep, padder = "|", " "
    final_row_width = sum([len(x) for x in padded_cells]) + (
        len(padded_cells) * len(sep)
    )
    extra_padding = TERMINAL_WIDTH - final_row_width - len(padded_cells)

    if padded_cells[0].strip() == TABLE_SEPARATOR[0]:
        padder = "-"
        padded_cells = [len(c) * padder for c in padded_cells]

    padding_per_cell = int(round(extra_padding / len(padded_cells)))
    to_join = []
    for index, cell in enumerate(padded_cells):
        alignment = colaligns[index]
        if alignment == "left":
            to_append = cell + (padder * padding_per_cell)

        elif alignment == "right":
            to_append = (padder * padding_per_cell) + cell

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
