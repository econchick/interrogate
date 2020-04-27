# Copyright 2020 Lynn Root
"""Measure and report on documentation coverage in Python modules."""
import ast
import os
import sys

import attr
import click
import tabulate

from py import io as py_io

from interrogate import config
from interrogate import utils
from interrogate import visit


tabulate.PRESERVE_WHITESPACE = True


@attr.s
class BaseInterrogateResult:
    """Base results class.

    :attr int total: total number of objects interrogated (modules,
        classes, methods, and functions).
    :attr int covered: number of objects covered by docstrings.
    :attr int missing: number of objects not covered by docstrings.
    :attr int skipped: number of modules skipped.
    """

    total = attr.ib(init=False, default=0)
    covered = attr.ib(init=False, default=0)
    missing = attr.ib(init=False, default=0)
    skipped = attr.ib(init=False, default=0)

    @property
    def perc_covered(self):
        """Percentage of node covered.

        :return: percentage covered over total.
        :rtype: float
        """
        if self.total == 0:
            return 0
        return (float(self.covered) / float(self.total)) * 100


@attr.s
class InterrogateFileResult(BaseInterrogateResult):
    """Coverage results for a particular file.

    :param str filename: filename associated with the coverage result.
    :param bool ignore_module: whether or not to ignore this file/module.
    :param visit.CoverageVisitor visitor: coverage visitor instance
        that assessed docstring coverage of file.
    """

    filename = attr.ib(default=None)
    ignore_module = attr.ib(default=False)
    visitor = attr.ib(repr=False, default=None)

    def combine(self):
        """Tally results from each AST node visited."""
        for node in self.visitor.graph.nodes:
            if node.node_type == "Module":
                if self.ignore_module:
                    self.skipped += 1
                    continue
            self.total += 1
            if node.covered:
                self.covered += 1

        self.missing = self.total - self.covered
        self.skipped = self.visitor.skipped


@attr.s
class InterrogateResults(BaseInterrogateResult):
    """Coverage results for all files.

    :attr int ret_code: return code of program (``0`` for success, ``1``
        for fail).
    :attr list(InterrogateFileResults) file_results: list of file
        results associated with this program run.
    """

    ret_code = attr.ib(init=False, default=0, repr=False)
    file_results = attr.ib(init=False, default=None, repr=False)

    def combine(self):
        """Tally results from each file."""
        for result in self.file_results:
            self.covered += result.covered
            self.missing += result.missing
            self.total += result.total
            self.skipped += result.skipped


class InterrogateCoverage:
    """The doc coverage interrogator!

    :param list(str) paths: list of paths to interrogate.
    :param config.InterrogateConfig conf: interrogation configuration.
    :param tuple(str) excluded: tuple of files and directories to exclude
        in assessing coverage.
    """

    COMMON_EXCLUDE = [".tox", ".venv", "venv", ".git", ".hg"]

    def __init__(self, paths, conf=None, excluded=None):
        self.paths = paths
        self.config = conf or config.InterrogateConfig()
        self.excluded = excluded or ()
        self.common_base = ""
        self._add_common_exclude()

    def _add_common_exclude(self):
        """Ignore common directories by default"""
        for path in self.paths:
            self.excluded = self.excluded + tuple(
                os.path.join(path, i) for i in self.COMMON_EXCLUDE
            )

    def _filter_files(self, files):
        """Filter files that are explicitly excluded."""
        for f in files:
            if not f.endswith(".py"):
                continue
            if self.config.ignore_init_module:
                basename = os.path.basename(f)
                if basename == "__init__.py":
                    continue
            maybe_excluded_dir = any(
                [f.startswith(exc) for exc in self.excluded]
            )
            maybe_excluded_file = f in self.excluded
            if any([maybe_excluded_dir, maybe_excluded_file]):
                continue
            yield f

    def get_filenames_from_paths(self):
        """Find all files to measure for docstring coverage."""
        filenames = []
        for path in self.paths:
            if os.path.isfile(path):
                if not path.endswith(".py"):
                    msg = (
                        "E: Invalid file '{}'. Unable interrogate non-Python "
                        "files.".format(path)
                    )
                    click.echo(msg)
                    return sys.exit(1)
                filenames.append(path)
                continue
            for root, dirs, fs in os.walk(path):
                full_paths = [os.path.join(root, f) for f in fs]
                filenames.extend(self._filter_files(full_paths))

        if not filenames:
            p = ", ".join(self.paths)
            click.echo(
                "E: No Python files found to interrogate in '{}'.".format(p)
            )
            return sys.exit(1)

        self.common_base = utils.get_common_base(filenames)
        return filenames

    def _get_file_coverage(self, filename):
        """Get coverage results for a particular file."""
        with open(filename, "r", encoding="utf-8") as f:
            source_tree = f.read()

        parsed_tree = ast.parse(source_tree)
        visitor = visit.CoverageVisitor(filename=filename, config=self.config)
        visitor.visit(parsed_tree)

        results = InterrogateFileResult(
            filename=filename,
            ignore_module=self.config.ignore_module,
            visitor=visitor,
        )
        results.combine()
        return results

    def _get_coverage(self, filenames):
        """Get coverage results."""
        results = InterrogateResults()
        if results.file_results is None:
            results.file_results = []
        for f in filenames:
            results.file_results.append(self._get_file_coverage(f))

        results.combine()

        if self.config.fail_under > results.perc_covered:
            results.ret_code = 1

        return results

    def get_coverage(self):
        """Get coverage results from files."""
        filenames = self.get_filenames_from_paths()
        return self._get_coverage(filenames)

    def _get_detailed_row(self, node, filename):
        """Generate a row of data for the detailed view."""
        padding = "  " * node.level

        filename = filename[len(self.common_base) + 1 :]
        name = "{} (module)".format(filename)
        if node.node_type != "Module":
            name = node.path.split(":")[-1]
            name = "{} (L{})".format(name, node.lineno)

        name = "{}{}".format(padding, name)
        status = "MISSED" if not node.covered else "COVERED"
        return [name, status]

    def _create_detailed_table(self, combined_results):
        """Generate table for the detailed view.

        The detailed view shows coverage of each module, class, and
        function/method.
        """
        verbose_tbl = []
        header = ["Name", "Status"]
        verbose_tbl.append(header)
        verbose_tbl.append(utils.TABLE_SEPARATOR)
        for file_result in combined_results.file_results:
            nodes = file_result.visitor.graph.nodes
            for n in nodes:
                verbose_tbl.append(
                    self._get_detailed_row(n, file_result.filename)
                )
            verbose_tbl.append(utils.TABLE_SEPARATOR)
        return verbose_tbl

    def _print_detailed_table(self, results, tw):
        """Print detailed table to the given output stream."""
        detailed_table = self._create_detailed_table(results)
        to_print = tabulate.tabulate(
            detailed_table,
            tablefmt=utils.InterrogateTableFormat,
            colalign=["left", "right"],
        )
        tw.sep("-", "Detailed Coverage")
        tw.line(to_print)
        tw.line()

    def _create_summary_table(self, combined_results):
        """Generate table for the summary view.

        The summary view shows coverage for an overall file.
        """
        table = []
        header = ["Name", "Total", "Miss", "Cover", "Cover%"]
        table.append(header)
        table.append(utils.TABLE_SEPARATOR)

        for file_result in combined_results.file_results:
            filename = file_result.filename[len(self.common_base) + 1 :]
            perc_covered = "{:.0f}%".format(file_result.perc_covered)
            row = [
                filename,
                file_result.total,
                file_result.missing,
                file_result.covered,
                perc_covered,
            ]
            table.append(row)

        table.append(utils.TABLE_SEPARATOR)
        total_perc_covered = "{:.1f}%".format(combined_results.perc_covered)
        total_row = [
            "TOTAL",
            combined_results.total,
            combined_results.missing,
            combined_results.covered,
            total_perc_covered,
        ]
        table.append(total_row)
        return table

    def _print_summary_table(self, results, tw):
        """Print summary table to the given output stream."""
        summary_table = self._create_summary_table(results)
        tw.sep("-", title="Summary")
        to_print = tabulate.tabulate(
            summary_table,
            tablefmt=utils.InterrogateTableFormat,
            colalign=("left", "right", "right", "right", "right"),
        )
        tw.line(to_print)

    def print_results(self, results, output, verbosity):
        """Print results to a given output stream.

        :param InterrogateResults results: results of docstring coverage
            interrogation.
        :param output: filename to output results. If ``None``, uses
            ``sys.stdout``.
        :type output: ``str`` or ``None``
        :param int verbosity: level of detail to print out (``0``-``2``).
        """
        with utils.smart_open(output, "w") as f:
            tw = py_io.TerminalWriter(file=f)
            if verbosity > 0:
                tw.sep("=", "Coverage for {}/".format(self.common_base))
            if verbosity > 1:
                self._print_detailed_table(results, tw)
            if verbosity > 0:
                self._print_summary_table(results, tw)

            status = "PASSED"
            if results.ret_code > 0:
                status = "FAILED"

            status_line = "RESULT: {} (minumum: {}%, actual: {:.1f}%)".format(
                status, self.config.fail_under, results.perc_covered
            )
            if verbosity > 0:
                tw.sep("-", title=status_line)
            else:
                tw.line(status_line)
