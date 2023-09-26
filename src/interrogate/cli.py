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
    show_default=False,
    help=(
        "Level of verbosity."
        "\n\nNOTE: When configuring verbosity in pyproject.toml or setup.cfg, "
        "`verbose=1` maps to `-v`, and `verbose=2` maps to `-vv`. "
        "`verbose=0` is the equivalent of no verbose flags used, producing "
        "minimal output."
    ),
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
    "-C",
    "--ignore-nested-classes",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore nested classes.",
)
@click.option(
    "-O",
    "--ignore-overloaded-functions",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore `@typing.overload`-decorated functions.",
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
    "-S",
    "--ignore-setters",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore methods with property setter decorators.",
)
@click.option(
    "-s",
    "--ignore-semiprivate",
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        "Ignore semiprivate classes, methods, and functions starting with a "
        "single underscore."
    ),
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
    "--omit-covered-files",
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        "Omit reporting files that have 100% documentation coverage. This "
        "option is ignored if verbosity is not set."
    ),
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
@click.option(
    "--badge-format",
    type=click.Choice(["svg", "png"], case_sensitive=False),
    default=None,
    show_default="svg",
    help=(
        "File format for the generated badge. Used with the "
        "`-g/--generate-badge` flag. [default: svg]"
        "\n\nNOTE: To generate a PNG file, interrogate must be installed "
        "with `interrogate[png]`, i.e. `pip install interrogate[png]`."
    ),
)
@click.option(
    "--badge-style",
    type=click.Choice(
        [
            "flat",
            "flat-square",
            "flat-square-modified",
            "for-the-badge",
            "plastic",
            "social",
        ],
        case_sensitive=False,
    ),
    default=None,
    help=(
        "Desired style of shields.io badge. Used with the "
        "`-g/--generate-badge` flag. [default: flat-square-modified]"
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
    .. versionchanged:: 1.3.1 only generate badge if results change from
        an existing badge.

    .. versionadded:: 1.1.3 ``--whitelist-regex``
    .. versionadded:: 1.2.0 ``--ignore-nested-functions``
    .. versionadded:: 1.2.0 ``--color``/``--no-color``
    .. versionadded:: 1.3.0 ``--ignore-property-decorators``
    .. versionadded:: 1.3.0 config parsing support for setup.cfg
    .. versionadded:: 1.4.0 ``--badge-format``
    .. versionadded:: 1.4.0 ``--ignore-nested-classes``
    .. versionadded:: 1.4.0 ``--ignore-setters``
    .. versionadded:: 1.5.0 ``--omit-covered-files``
    .. versionadded:: 1.5.0 ``--badge-style``
    .. versionadded:: 1.6.0 ``--ignore-overloaded-functions``

    .. versionchanged:: 1.3.1 only generate badge if results change from
        an existing badge.
    """
    gen_badge = kwargs["generate_badge"]
    if kwargs["badge_format"] is not None and gen_badge is None:
        raise click.BadParameter(
            "The `--badge-format` option must be used along with the `-g/"
            "--generate-badge option."
        )
    if kwargs["badge_style"] is not None and gen_badge is None:
        raise click.BadParameter(
            "The `--badge-style` option must be used along with the `-g/"
            "--generate-badge option."
        )
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
        color=kwargs["color"],
        fail_under=kwargs["fail_under"],
        ignore_regex=kwargs["ignore_regex"],
        ignore_magic=kwargs["ignore_magic"],
        ignore_module=kwargs["ignore_module"],
        ignore_private=kwargs["ignore_private"],
        ignore_semiprivate=kwargs["ignore_semiprivate"],
        ignore_init_method=kwargs["ignore_init_method"],
        ignore_init_module=kwargs["ignore_init_module"],
        ignore_nested_classes=kwargs["ignore_nested_classes"],
        ignore_nested_functions=kwargs["ignore_nested_functions"],
        ignore_overloaded_functions=kwargs["ignore_overloaded_functions"],
        ignore_property_setters=kwargs["ignore_setters"],
        ignore_property_decorators=kwargs["ignore_property_decorators"],
        include_regex=kwargs["whitelist_regex"],
        omit_covered_files=kwargs["omit_covered_files"],
    )
    interrogate_coverage = coverage.InterrogateCoverage(
        paths=paths,
        conf=conf,
        excluded=kwargs["exclude"],
    )
    results = interrogate_coverage.get_coverage()

    is_quiet = kwargs["quiet"]
    if not is_quiet:
        colorama.init()  # needed for Windows
        interrogate_coverage.print_results(
            results, kwargs["output"], kwargs["verbose"]
        )

    if gen_badge is not None:
        badge_format = kwargs["badge_format"]
        badge_style = kwargs["badge_style"]
        output_path = badge_gen.create(
            gen_badge,
            results,
            output_format=badge_format,
            output_style=badge_style,
        )
        if not is_quiet:
            click.echo(f"Generated badge to {output_path}")

    sys.exit(results.ret_code)
