# Copyright 2020-2024 Lynn Root
"""Measure and report on documentation coverage in Python modules."""

from __future__ import annotations

import ast
import decimal
import fnmatch
import os
import sys

from typing import Final, Iterator

import attr
import click
import tabulate

from interrogate import config, utils, visit


tabulate.PRESERVE_WHITESPACE = True


@attr.s
class BaseInterrogateResult:
    """Base results class.

    :attr int total: total number of objects interrogated (modules,
        classes, methods, and functions).
    :attr int covered: number of objects covered by docstrings.
    :attr int missing: number of objects not covered by docstrings.
    """

    total: int = attr.ib(init=False, default=0)
    covered: int = attr.ib(init=False, default=0)
    missing: int = attr.ib(init=False, default=0)

    @property
    def perc_covered(self) -> float:
        """Percentage of node covered.

        .. versionchanged:: 1.3.2
        A total of 0 translates to 100% coverage now

        :return: percentage covered over total.
        :rtype: float
        """
        # Even though empty files each have a total of one,
        # the ignore-module option may still lead to a total of zero.
        if self.total == 0:  # pragma: no cover
            return 100.0
        return (float(self.covered) / float(self.total)) * 100


@attr.s
class InterrogateFileResult(BaseInterrogateResult):
    """Coverage results for a particular file.

    :param str filename: filename associated with the coverage result.
    :param bool ignore_module: whether or not to ignore this file/module.
    :param list[visit.CovNode] nodes: visited AST nodes.
    """

    filename: str = attr.ib(default=None)
    ignore_module: bool = attr.ib(default=False)
    nodes: list[visit.CovNode] = attr.ib(repr=False, default=None)

    def combine(self) -> None:
        """Tally results from each AST node visited."""
        for node in self.nodes:
            if node.node_type == "Module":
                if self.ignore_module:
                    continue
            self.total += 1
            if node.covered:
                self.covered += 1

        self.missing = self.total - self.covered


@attr.s
class InterrogateResults(BaseInterrogateResult):
    """Coverage results for all files.

    :attr int ret_code: return code of program (``0`` for success, ``1``
        for fail).
    :attr list(InterrogateFileResult) file_results: list of file
        results associated with this program run.
    """

    ret_code: int = attr.ib(init=False, default=0, repr=False)
    file_results: list[InterrogateFileResult] = attr.ib(
        init=False, default=None, repr=False
    )

    def combine(self) -> None:
        """Tally results from each file."""
        for result in self.file_results:
            self.covered += result.covered
            self.missing += result.missing
            self.total += result.total


class InterrogateCoverage:
    """The doc coverage interrogator!

    :param list(str) paths: list of paths to interrogate.
    :param config.InterrogateConfig conf: interrogation configuration.
    :param tuple(str) excluded: tuple of files and directories to exclude
        in assessing coverage.
    :param list[str] extensions: additional file extensions to interrogate.
    """

    COMMON_EXCLUDE: Final[list[str]] = [".tox", ".venv", "venv", ".git", ".hg"]
    VALID_EXT: Final[list[str]] = [
        ".py",
        ".pyi",
    ]  # someday in the future: .ipynb

    def __init__(
        self,
        paths: list[str],
        conf: config.InterrogateConfig | None = None,
        excluded: tuple[str] | None = None,
        extensions: tuple[str] | None = None,
    ):
        self.paths = paths
        self.extensions = set(extensions or set())
        self.extensions.add(".py")
        self.config = conf or config.InterrogateConfig()
        self.excluded = excluded or ()
        self.common_base = ""
        self._add_common_exclude()
        self.skipped_file_count = 0
        self.output_formatter: utils.OutputFormatter

    def _add_common_exclude(self) -> None:
        """Ignore common directories by default"""
        for path in self.paths:
            self.excluded = self.excluded + tuple(  # type: ignore
                os.path.join(path, i) for i in self.COMMON_EXCLUDE
            )

    def _filter_files(self, files: list[str]) -> Iterator[str]:
        """Filter files that are explicitly excluded."""
        for f in files:
            has_valid_ext = any([f.endswith(ext) for ext in self.extensions])
            if not has_valid_ext:
                continue
            if self.config.ignore_init_module:
                basename = os.path.basename(f)
                if basename == "__init__.py":
                    continue
            if any(fnmatch.fnmatch(f, exc + "*") for exc in self.excluded):
                continue
            yield f

    def get_filenames_from_paths(self) -> list[str]:
        """Find all files to measure for docstring coverage."""
        filenames = []
        for path in self.paths:
            if os.path.isfile(path):
                has_valid_ext = any(
                    [path.endswith(ext) for ext in self.VALID_EXT]
                )
                if not has_valid_ext:
                    msg = (
                        f"E: Invalid file '{path}'. Unable to interrogate "
                        "non-Python or Python-like files. "
                        f"Valid file extensions: {', '.join(self.VALID_EXT)}"
                    )
                    click.echo(msg, err=True)
                    return sys.exit(1)
                filenames.append(path)
                continue
            for root, dirs, fs in os.walk(path):
                full_paths = [os.path.join(root, f) for f in fs]
                filenames.extend(self._filter_files(full_paths))

        if not filenames:
            p = ", ".join(self.paths)
            msg = (
                f"E: No Python or Python-like files found to interrogate in "
                f"'{p}'."
            )
            click.echo(msg, err=True)
            return sys.exit(1)

        self.common_base = utils.get_common_base(filenames)
        return filenames

    def _filter_nodes(self, nodes: list[visit.CovNode]) -> list[visit.CovNode]:
        """Remove empty modules when ignoring modules."""
        is_empty = 1 == len(nodes)
        if is_empty and self.config.ignore_module:
            return []

        if not self.config.include_regex:
            return nodes

        # FIXME: any methods, closures, inner functions/classes, etc
        #        will print out with extra indentation if the parent
        #        does not meet the whitelist
        filtered = []
        module_node = None
        for node in nodes:
            if node.node_type == "Module":
                module_node = node
                continue
            for regexp in self.config.include_regex:
                match = regexp.match(node.name)
                if match:
                    filtered.append(node)
        if module_node and filtered:
            filtered.insert(0, module_node)
        return filtered

    def _filter_inner_nested(
        self, nodes: list[visit.CovNode]
    ) -> list[visit.CovNode]:
        """Filter out children of ignored nested funcs/classes."""
        nested_cls = [n for n in nodes if n.is_nested_cls]
        inner_nested_nodes = [n for n in nodes if n.parent in nested_cls]

        filtered_nodes = [n for n in nodes if n not in inner_nested_nodes]
        filtered_nodes = [n for n in filtered_nodes if n not in nested_cls]
        return filtered_nodes

    def _set_google_style(self, nodes: list[visit.CovNode]) -> None:
        """Apply Google-style docstrings for class coverage.

        Update coverage of a class node if its `__init__` method has a
        docstring, or an `__init__` method if its class has a docstring.

        A class and its `__init__` method are considered covered if either one
        contains a docstring. See <https://sphinxcontrib-napoleon.readthedocs.
        io/en/latest/example_google.html>`_ for more info and an example.
        """
        for node in nodes:
            if node.node_type == "FunctionDef" and node.name == "__init__":
                if not node.covered and node.parent.covered:  # type: ignore
                    setattr(node, "covered", True)
                elif node.covered and not node.parent.covered:  # type: ignore
                    setattr(node.parent, "covered", True)

    def _get_file_coverage(
        self, filename: str
    ) -> InterrogateFileResult | None:
        """Get coverage results for a particular file."""
        with open(filename, encoding="utf-8") as f:
            source_tree = f.read()

        parsed_tree = ast.parse(source_tree)
        visitor = visit.CoverageVisitor(filename=filename, config=self.config)
        visitor.visit(parsed_tree)

        filtered_nodes = self._filter_nodes(visitor.nodes)
        if len(filtered_nodes) == 0:
            return None

        if self.config.ignore_nested_functions:
            filtered_nodes = [
                n for n in filtered_nodes if not n.is_nested_func
            ]
        if self.config.ignore_nested_classes:
            filtered_nodes = self._filter_inner_nested(filtered_nodes)

        if self.config.docstring_style == "google":
            self._set_google_style(filtered_nodes)

        results = InterrogateFileResult(
            filename=filename,
            ignore_module=self.config.ignore_module,
            nodes=filtered_nodes,
        )
        results.combine()
        return results

    def _get_coverage(self, filenames: list[str]) -> InterrogateResults:
        """Get coverage results."""
        results = InterrogateResults()
        file_results = []
        for f in filenames:
            result = self._get_file_coverage(f)
            if result:
                file_results.append(result)
        results.file_results = file_results

        results.combine()

        fail_under_str = str(self.config.fail_under)
        fail_under_dec = decimal.Decimal(fail_under_str)
        round_to = -fail_under_dec.as_tuple().exponent  # type: ignore

        if self.config.fail_under > round(results.perc_covered, round_to):
            results.ret_code = 1

        return results

    def get_coverage(self) -> InterrogateResults:
        """Get coverage results from files."""
        filenames = self.get_filenames_from_paths()
        return self._get_coverage(filenames)

    def _get_filename(self, filename: str) -> str:
        """Get filename for output information.

        If only one file is being interrogated, then ``self.common_base``
        and ``filename`` will be the same. Therefore, take the file
        ``os.path.basename`` as the return ``filename``.
        """
        if filename == self.common_base:
            return os.path.basename(filename)
        return filename[len(self.common_base) + 1 :]

    def _get_detailed_row(
        self, node: visit.CovNode, filename: str
    ) -> list[str]:
        """Generate a row of data for the detailed view."""
        filename = self._get_filename(filename)

        if node.node_type == "Module":
            if self.config.ignore_module:
                return [filename, ""]
            name = f"{filename} (module)"
        else:
            name = node.path.split(":")[-1]
            name = f"{name} (L{node.lineno})"

        padding = "  " * node.level
        name = f"{padding}{name}"
        status = "MISSED" if not node.covered else "COVERED"
        return [name, status]

    def _create_detailed_table(
        self, combined_results: InterrogateResults
    ) -> list[list[str]]:
        """Generate table for the detailed view.

        The detailed view shows coverage of each module, class, and
        function/method.
        """

        def _sort_nodes(x: visit.CovNode) -> int:
            """Sort nodes by line number."""
            lineno = getattr(x, "lineno", 0)
            # lineno is "None" if module is empty
            if lineno is None:
                lineno = 0
            return lineno

        verbose_tbl = []
        header = ["Name", "Status"]
        verbose_tbl.append(header)
        verbose_tbl.append(self.output_formatter.TABLE_SEPARATOR)
        for file_result in combined_results.file_results:
            if (
                self.config.omit_covered_files
                and file_result.perc_covered == 100
            ):
                continue
            nodes = file_result.nodes
            nodes = sorted(nodes, key=_sort_nodes)
            for n in nodes:
                verbose_tbl.append(
                    self._get_detailed_row(n, file_result.filename)
                )
            verbose_tbl.append(self.output_formatter.TABLE_SEPARATOR)
        return verbose_tbl

    def _print_detailed_table(self, results: InterrogateResults) -> None:
        """Print detailed table to the given output stream."""
        detailed_table = self._create_detailed_table(results)

        # don't print an empty table if --omit-covered & all files have 100%
        if len(detailed_table) < 3:
            return

        to_print = tabulate.tabulate(
            detailed_table,
            tablefmt=self.output_formatter.get_table_formatter(
                table_type="detailed"
            ),
            colalign=["left", "right"],
        )
        self.output_formatter.tw.sep(
            "-",
            "Detailed Coverage",
            fullwidth=self.output_formatter.TERMINAL_WIDTH,
        )
        self.output_formatter.tw.line(to_print)
        self.output_formatter.tw.line()

    def _create_summary_table(
        self, combined_results: InterrogateResults
    ) -> list[list[str]]:
        """Generate table for the summary view.

        The summary view shows coverage for an overall file.
        """
        table = []
        header = ["Name", "Total", "Miss", "Cover", "Cover%"]
        table.append(header)
        table.append(self.output_formatter.TABLE_SEPARATOR)

        for file_result in combined_results.file_results:
            filename = self._get_filename(file_result.filename)
            if (
                self.config.omit_covered_files
                and file_result.perc_covered == 100
            ):
                continue
            perc_covered = f"{file_result.perc_covered:.0f}%"
            row = [
                filename,
                str(file_result.total),
                str(file_result.missing),
                str(file_result.covered),
                perc_covered,
            ]
            table.append(row)

        # avoid printing an unneeded second separator if there are
        # no summary results from --omit-covered
        if len(table) > 2:
            table.append(self.output_formatter.TABLE_SEPARATOR)

        total_perc_covered = f"{combined_results.perc_covered:.1f}%"
        total_row = [
            "TOTAL",
            str(combined_results.total),
            str(combined_results.missing),
            str(combined_results.covered),
            total_perc_covered,
        ]
        table.append(total_row)
        return table

    def _print_summary_table(self, results: InterrogateResults) -> None:
        """Print summary table to the given output stream."""
        summary_table = self._create_summary_table(results)
        self.output_formatter.tw.sep(
            "-",
            title="Summary",
            fullwidth=self.output_formatter.TERMINAL_WIDTH,
        )
        to_print = tabulate.tabulate(
            summary_table,
            tablefmt=self.output_formatter.get_table_formatter(
                table_type="summary"
            ),
            colalign=("left", "right", "right", "right", "right"),
        )
        self.output_formatter.tw.line(to_print)

    @staticmethod
    def _sort_results(results: InterrogateResults) -> InterrogateResults:
        """Sort results by filename, directories first"""
        all_filenames_map = {r.filename: r for r in results.file_results}
        all_dirs = sorted(
            {
                os.path.dirname(r.filename)
                for r in results.file_results
                if os.path.dirname(r.filename) != ""
            }
        )

        sorted_results = []
        while all_dirs:
            current_dir = all_dirs.pop(0)
            files = []
            for p in os.listdir(current_dir):
                path = os.path.join(current_dir, p)
                if path in all_filenames_map.keys():
                    files.append(path)
            files = sorted(files)
            sorted_results.extend(files)

        sorted_res = []
        for filename in sorted_results:
            sorted_res.append(all_filenames_map[filename])
        results.file_results = sorted_res
        return results

    def _get_header_base(self) -> str:
        """Get common base directory for header of verbose output."""
        base = self.common_base
        if os.path.isfile(base):
            base = os.path.dirname(base)
        if sys.platform in ("cygwin", "win32"):  # pragma: no cover
            return base + "\\"
        return base + "/"

    def _print_omitted_file_count(self, results: InterrogateResults) -> None:
        """Print # of files omitted due to 100% coverage and --omit-covered.

        :param InterrogateResults results: results of docstring coverage
            interrogation.
        """
        if not self.config.omit_covered_files:
            return

        omitted_files = [
            r for r in results.file_results if r.perc_covered == 100
        ]
        omitted_file_count = len(omitted_files)
        if omitted_file_count == 0:
            return

        total_files_scanned = len(results.file_results)
        files_humanized = "files" if total_files_scanned > 1 else "file"
        files_skipped = (
            f"({omitted_file_count} of {total_files_scanned} {files_humanized} "
            "omitted due to complete coverage)"
        )
        to_print = tabulate.tabulate(
            [self.output_formatter.TABLE_SEPARATOR, [files_skipped]],
            tablefmt=self.output_formatter.get_table_formatter(
                table_type="summary"
            ),
            colalign=("center",),
        )
        self.output_formatter.tw.line(to_print)

    def print_results(
        self, results: InterrogateResults, output: str | None, verbosity: int
    ) -> None:
        """Print results to a given output stream.

        :param InterrogateResults results: results of docstring coverage
            interrogation.
        :param output: filename to output results. If ``None``, uses
            ``sys.stdout``.
        :type output: ``str`` or ``None``
        :param int verbosity: level of detail to print out (``0``-``2``).
        """
        with utils.smart_open(output, "w") as f:
            self.output_formatter = utils.OutputFormatter(
                file=f, config=self.config
            )
            results = self._sort_results(results)
            if verbosity > 0:
                base = self._get_header_base()
                self.output_formatter.tw.sep(
                    "=",
                    f"Coverage for {base}",
                    fullwidth=self.output_formatter.TERMINAL_WIDTH,
                )
            if verbosity > 1:
                self._print_detailed_table(results)
            if verbosity > 0:
                self._print_summary_table(results)

            status, color = "PASSED", {"green": True}
            if results.ret_code > 0:
                status, color = "FAILED", {"red": True}

            if self.output_formatter.should_markup() is False:
                color = {}

            status_line = "RESULT: {} (minimum: {}%, actual: {:.1f}%)".format(
                status, self.config.fail_under, results.perc_covered
            )
            if verbosity > 0:
                self._print_omitted_file_count(results)

                self.output_formatter.tw.sep(
                    "-",
                    title=status_line,
                    fullwidth=self.output_formatter.TERMINAL_WIDTH,
                    **color,
                )
            else:
                self.output_formatter.tw.line(status_line)
