# Copyright 2020 Lynn Root
"""CLI entrypoint into `interrogate`."""

import os
import sys

from pathlib import Path

import click

from interrogate import __version__ as version
from interrogate import badge_gen
from interrogate import config
from interrogate import coverage
from interrogate import utils


@click.command()
@click.version_option(version, prog_name="interrogate")
@click.option(
    "-v",
    "--verbose",
    default=0,
    count=True,
    show_default=True,
    help="Level of verbosity",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    show_default=True,
    help="Do not print output",
)
@click.option(
    "-f",
    "--fail-under",
    type=float,
    metavar="INT | FLOAT",
    default=80.0,
    show_default=True,
    help="Fail when coverage % is less than a given amount.",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    default=(),
    help=(
        "Exclude PATHs of files and/or directories. Multiple `-e/--exclude` "
        "invocations supported."
    ),
)
@click.option(
    "-i",
    "--ignore-init-method",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore `__init__` method of classes.",
)
@click.option(
    "-I",
    "--ignore-init-module",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore `__init__.py` modules.",
)
@click.option(
    "-m",
    "--ignore-magic",
    is_flag=True,
    default=False,
    show_default=False,
    help=(
        "Ignore all magic methods of classes.  [default: False]\n\nNOTE: This "
        "does not include the `__init__` method. To ignore `__init__` methods, "
        "use `--ignore-init-method`."
    ),
)
@click.option(
    "-M",
    "--ignore-module",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore module-level docstrings.",
)
@click.option(
    "-p",
    "--ignore-private",
    is_flag=True,
    default=False,
    show_default=False,
    help=(
        "Ignore private classes, methods, and functions starting with two "
        "underscores.  [default:False]"
        "\n\nNOTE: This does not include magic methods; use `--ignore-magic` "
        "and/or `--ignore-init-method` instead."
    ),
)
@click.option(
    "-s",
    "--ignore-semiprivate",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore semiprivate classes, methods, and functions starting with a "
    "single underscore.",
)
@click.option(
    "-r",
    "--ignore-regex",
    type=str,
    default=(),
    multiple=True,
    metavar="STR",
    callback=utils.parse_regex,
    help=(
        "Regex identifying class, method, and function names to ignore. "
        "Multiple `-r/--ignore-regex` invocations supported."
    ),
)
@click.option(
    "-w",
    "--whitelist-regex",
    type=str,
    default=(),
    multiple=True,
    metavar="STR",
    callback=utils.parse_regex,
    help=(
        "Regex identifying class, method, and function names to include. "
        "Multiple `-w/--whitelist-regex` invocations supported."
    ),
)
@click.option(
    "-o",
    "--output",
    default=None,
    metavar="FILE",
    help="Write output to a given FILE.  [default: stdout]",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, readable=True
    ),
    is_eager=True,
    callback=config.read_pyproject_toml,
    help="Read configuration from `pyproject.toml`.",
)
@click.option(
    "-g",
    "--generate-badge",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
    default=None,
    help=(
        "Generate a 'shields.io' status badge (an SVG image) in at a given "
        "file or directory."
    ),
)
@click.help_option("-h", "--help")
@click.argument(
    "paths",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    nargs=-1,
)
def main(paths, **kwargs):
    """Measure and report on documentation coverage in Python modules.

    \f
    # below the "\f" is ignored when running ``interrogate --help``

    .. versionchanged:: 1.1.3 ``--ignore-regex`` may now accept multiple
        values.

    .. versionadded:: 1.1.3 ``--whitelist-regex``
    """
    if not paths:
        paths = (Path.cwd(),)
    else:
        paths = tuple(Path(p) for p in paths)

    # NOTE: this will need to be fixed if we want to start supporting
    #       --whitelist-regex on filenames. This otherwise assumes you
    #       want to ignore module-level docs when only white listing
    #       items (visit.py will also need to be addressed since white/
    #       black listing only looks at classes & funcs, not modules).
    if kwargs["whitelist_regex"]:
        kwargs["ignore_module"] = True

    conf = config.InterrogateConfig(
        ignore_init_method=kwargs["ignore_init_method"],
        ignore_init_module=kwargs["ignore_init_module"],
        ignore_magic=kwargs["ignore_magic"],
        ignore_module=kwargs["ignore_module"],
        ignore_private=kwargs["ignore_private"],
        ignore_regex=kwargs["ignore_regex"],
        ignore_semiprivate=kwargs["ignore_semiprivate"],
        fail_under=kwargs["fail_under"],
        include_regex=kwargs["whitelist_regex"],
    )
    interrogate_coverage = coverage.InterrogateCoverage(
        paths=paths, conf=conf, excluded=kwargs["exclude"],
    )
    results = interrogate_coverage.get_coverage()

    is_quiet = kwargs["quiet"]
    if not is_quiet:
        interrogate_coverage.print_results(
            results, kwargs["output"], kwargs["verbose"]
        )

    if kwargs["generate_badge"] is not None:
        output_path = badge_gen.create(kwargs["generate_badge"], results)
        if not is_quiet:
            click.echo("Generated badge to {}".format(output_path))

    sys.exit(results.ret_code)
