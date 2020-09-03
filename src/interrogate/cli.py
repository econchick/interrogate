# Copyright 2020 Lynn Root
"""CLI entrypoint into `interrogate`."""

import os
import sys

import click

import colorama

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
    "-n",
    "--ignore-nested-functions",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore nested functions and methods.",
)
@click.option(
    "-p",
    "--ignore-private",
    is_flag=True,
    default=False,
    show_default=False,
    help=(
        "Ignore private classes, methods, and functions starting with two "
        "underscores.  [default: False]"
        "\n\nNOTE: This does not include magic methods; use `--ignore-magic` "
        "and/or `--ignore-init-method` instead."
    ),
)
@click.option(
    "-P",
    "--ignore-property-decorators",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore methods with property setter/getter decorators.",
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
    "--color/--no-color",
    is_flag=True,
    default=True,
    show_default=True,
    envvar="INTERROGATE_COLOR",
    help="Toggle color output on/off when printing to stdout.",
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
        "file or directory. Will not generate a badge if results did not "
        "change from an existing badge of the same path."
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
    is_eager=True,
    nargs=-1,
)
@click.option(
    "-c",
    "--config",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, readable=True
    ),
    is_eager=True,
    callback=config.read_config_file,
    help="Read configuration from `pyproject.toml` or `setup.cfg`.",
)
@click.pass_context
def main(ctx, paths, **kwargs):
    """Measure and report on documentation coverage in Python modules.

    \f
    # below the "\f" is ignored when running ``interrogate --help``

    .. versionchanged:: 1.1.3 ``--ignore-regex`` may now accept multiple
        values.

    .. versionadded:: 1.1.3 ``--whitelist-regex``
    .. versionadded:: 1.2.0 ``--ignore-nested-functions``
    .. versionadded:: 1.2.0 ``--color``/``--no-color``
    .. versionadded:: 1.3.0 ``--ignore-property-decorators``
    .. versionadded:: 1.3.0 config parsing support for setup.cfg

    .. versionchanged:: 1.3.1 only generate badge if results change from
        an existing badge.
    """
    if not paths:
        paths = (os.path.abspath(os.getcwd()),)

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
        ignore_nested_functions=kwargs["ignore_nested_functions"],
        ignore_property_decorators=kwargs["ignore_property_decorators"],
        ignore_private=kwargs["ignore_private"],
        ignore_regex=kwargs["ignore_regex"],
        ignore_semiprivate=kwargs["ignore_semiprivate"],
        fail_under=kwargs["fail_under"],
        include_regex=kwargs["whitelist_regex"],
        color=kwargs["color"],
    )
    interrogate_coverage = coverage.InterrogateCoverage(
        paths=paths, conf=conf, excluded=kwargs["exclude"],
    )
    results = interrogate_coverage.get_coverage()

    is_quiet = kwargs["quiet"]
    if not is_quiet:
        colorama.init()  # needed for Windows
        interrogate_coverage.print_results(
            results, kwargs["output"], kwargs["verbose"]
        )

    if kwargs["generate_badge"] is not None:
        output_path = badge_gen.create(kwargs["generate_badge"], results)
        if not is_quiet:
            click.echo("Generated badge to {}".format(output_path))

    sys.exit(results.ret_code)
