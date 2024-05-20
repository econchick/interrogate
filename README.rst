.. image:: https://interrogate.readthedocs.io/en/latest/_static/logo_pink.png
    :alt: Pink Sloth Logo

=================================
``interrogate``: explain yourself
=================================

.. image:: https://interrogate.readthedocs.io/en/latest/_static/interrogate_badge.svg
   :target: https://github.com/econchick/interrogate
   :alt: Documentation Coverage

.. image:: https://codecov.io/gh/econchick/interrogate/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/econchick/interrogate
   :alt: Testing Coverage

.. image:: https://readthedocs.org/projects/interrogate/badge/?version=latest&style=flat
   :target: https://interrogate.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/econchick/interrogate/workflows/CI/badge.svg?branch=master
   :target: https://github.com/econchick/interrogate/actions?workflow=CI
   :alt: CI Status

.. image:: https://results.pre-commit.ci/badge/github/econchick/interrogate/master.svg
   :target: https://results.pre-commit.ci/latest/github/econchick/interrogate/master
   :alt: pre-commit.ci status

.. start-readme

Interrogate a codebase for docstring coverage.

Why Do I Need This?
===================

``interrogate`` checks your code base for missing docstrings.

Documentation should be as important as code itself. And it should live *within* code. Python `standardized <https://www.python.org/dev/peps/pep-0257/>`_ docstrings, allowing for developers to navigate libraries as simply as calling ``help()`` on objects, and with powerful tools like `Sphinx <https://www.sphinx-doc.org/en/master/>`_, `pydoc <https://docs.python.org/3/library/pydoc.html>`_, and `Docutils <https://docutils.sourceforge.io/>`_ to automatically generate HTML, LaTeX, PDFs, etc.

*Enter:* ``interrogate``.

``interrogate`` will tell you which methods, functions, classes, and modules have docstrings, and which do not. Use ``interrogate`` to:

* Get an understanding of how well your code is documented;
* Add it to CI/CD checks to enforce documentation on newly-added code;
* Assess a new code base for (one aspect of) code quality and maintainability.

Let's get started.

Requirements
============

``interrogate`` supports Python 3.8 and above.


Installation
============

``interrogate`` is available on `PyPI <https://pypi.org/project/interrogate/>`_ and `GitHub <https://github.com/econchick/interrogate>`_. The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a `virtualenv <https://hynek.me/articles/virtualenv-lives/>`_:

.. code-block:: console

    $ pip install interrogate

Extras
------

``interrogate`` provides a way to generate a `shields.io-like coverage badge <#other-usage>`_ as an **SVG file**.
To generate a **PNG file** instead, install ``interrogate`` with the extras ``[png]``:

.. code-block:: console

    $ pip install interrogate[png]

**NOTICE:** Additional system libraries/tools may be required in order to generate a PNG file of the coverage badge:

* on Windows, install Visual C++ compiler for Cairo;
* on macOS, install ``cairo`` and ``libffi`` (with Homebrew for example - `see note below <#macos-and-cairo>`_);
* on Linux, install the ``cairo``, ``python3-dev`` and ``libffi-dev`` packages (names may vary depending on distribution).

Refer to the ``cairosvg`` `documentation <https://cairosvg.org/documentation/>`_ for more information.

MacOS and Cairo
^^^^^^^^^^^^^^^

If you get an error when trying to generate a badge like so:

.. code-block:: console

    OSError: no library called "cairo-2" was found
    no library called "cairo" was found
    no library called "libcairo-2" was found


Then first try:

.. code-block:: console

    export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib

And rerun the command.

Usage
=====

Try it out on a Python project:

.. code-block:: console

    $ interrogate [PATH]
    RESULT: PASSED (minimum: 80.0%, actual: 100.0%)


Add verbosity to see a summary:

.. code-block:: console

    $ interrogate -v [PATH]

    ================== Coverage for /Users/lynn/dev/interrogate/ ====================
    ------------------------------------ Summary ------------------------------------
    | Name                                  |   Total |   Miss |   Cover |   Cover% |
    |---------------------------------------|---------|--------|---------|----------|
    | src/interrogate/__init__.py           |       1 |      0 |       1 |     100% |
    | src/interrogate/__main__.py           |       1 |      0 |       1 |     100% |
    | src/interrogate/badge_gen.py          |       6 |      0 |       6 |     100% |
    | src/interrogate/cli.py                |       2 |      0 |       2 |     100% |
    | src/interrogate/config.py             |       8 |      0 |       8 |     100% |
    | src/interrogate/coverage.py           |      27 |      0 |      27 |     100% |
    | src/interrogate/utils.py              |      10 |      0 |      10 |     100% |
    | src/interrogate/visit.py              |      18 |      0 |      18 |     100% |
    | tests/functional/__init__.py          |       1 |      0 |       1 |     100% |
    | tests/functional/test_cli.py          |       8 |      0 |       8 |     100% |
    | tests/functional/test_coverage.py     |      10 |      0 |      10 |     100% |
    | tests/unit/__init__.py                |       1 |      0 |       1 |     100% |
    | tests/unit/test_badge_gen.py          |       8 |      0 |       8 |     100% |
    | tests/unit/test_config.py             |      10 |      0 |      10 |     100% |
    | tests/unit/test_utils.py              |      13 |      0 |      13 |     100% |
    |---------------------------------------|---------|--------|---------|----------|
    | TOTAL                                 |     124 |      0 |     124 |   100.0% |
    ---------------- RESULT: PASSED (minimum: 80.0%, actual: 100.0%) ----------------


Add even *more* verbosity:


.. code-block:: console

    $ interrogate -vv [PATH]

    ================== Coverage for /Users/lynn/dev/interrogate/ ====================
    ------------------------------- Detailed Coverage -------------------------------
    | Name                                                                |  Status |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/__init__.py (module)                                | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/__main__.py (module)                                | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/badge_gen.py (module)                               | COVERED |
    |   save_badge (L42)                                                  | COVERED |
    |   get_badge (L87)                                                   | COVERED |
    |   should_generate_badge (L103)                                      | COVERED |
    |   get_color (L160)                                                  | COVERED |
    |   create (L173)                                                     | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/cli.py (module)                                     | COVERED |
    |   main (L258)                                                       | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/config.py (module)                                  | COVERED |
    |   InterrogateConfig (L19)                                           | COVERED |
    |   find_project_root (L61)                                           | COVERED |
    |   find_project_config (L89)                                         | COVERED |
    |   parse_pyproject_toml (L100)                                       | COVERED |
    |   sanitize_list_values (L116)                                       | COVERED |
    |   parse_setup_cfg (L139)                                            | COVERED |
    |   read_config_file (L173)                                           | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/coverage.py (module)                                | COVERED |
    |   BaseInterrogateResult (L23)                                       | COVERED |
    |     BaseInterrogateResult.perc_covered (L37)                        | COVERED |
    |   InterrogateFileResult (L54)                                       | COVERED |
    |     InterrogateFileResult.combine (L67)                             | COVERED |
    |   InterrogateResults (L81)                                          | COVERED |
    |     InterrogateResults.combine (L93)                                | COVERED |
    |   InterrogateCoverage (L101)                                        | COVERED |
    |     InterrogateCoverage._add_common_exclude (L121)                  | COVERED |
    |     InterrogateCoverage._filter_files (L128)                        | COVERED |
    |     InterrogateCoverage.get_filenames_from_paths (L141)             | COVERED |
    |     InterrogateCoverage._filter_nodes (L168)                        | COVERED |
    |     InterrogateCoverage._filter_inner_nested (L194)                 | COVERED |
    |     InterrogateCoverage._get_file_coverage (L203)                   | COVERED |
    |     InterrogateCoverage._get_coverage (L231)                        | COVERED |
    |     InterrogateCoverage.get_coverage (L248)                         | COVERED |
    |     InterrogateCoverage._get_filename (L253)                        | COVERED |
    |     InterrogateCoverage._get_detailed_row (L264)                    | COVERED |
    |     InterrogateCoverage._create_detailed_table (L281)               | COVERED |
    |       InterrogateCoverage._create_detailed_table._sort_nodes (L288) | COVERED |
    |     InterrogateCoverage._print_detailed_table (L315)                | COVERED |
    |     InterrogateCoverage._create_summary_table (L338)                | COVERED |
    |     InterrogateCoverage._print_summary_table (L381)                 | COVERED |
    |     InterrogateCoverage._sort_results (L399)                        | COVERED |
    |     InterrogateCoverage._get_header_base (L429)                     | COVERED |
    |     InterrogateCoverage._print_omitted_file_count (L438)            | COVERED |
    |     InterrogateCoverage.print_results (L469)                        | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/utils.py (module)                                   | COVERED |
    |   parse_regex (L21)                                                 | COVERED |
    |   smart_open (L40)                                                  | COVERED |
    |   get_common_base (L60)                                             | COVERED |
    |   OutputFormatter (L80)                                             | COVERED |
    |     OutputFormatter.should_markup (L90)                             | COVERED |
    |     OutputFormatter.set_detailed_markup (L105)                      | COVERED |
    |     OutputFormatter.set_summary_markup (L129)                       | COVERED |
    |     OutputFormatter._interrogate_line_formatter (L158)              | COVERED |
    |     OutputFormatter.get_table_formatter (L226)                      | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/visit.py (module)                                   | COVERED |
    |   CovNode (L15)                                                     | COVERED |
    |   CoverageVisitor (L44)                                             | COVERED |
    |     CoverageVisitor._has_doc (L58)                                  | COVERED |
    |     CoverageVisitor._visit_helper (L65)                             | COVERED |
    |     CoverageVisitor._is_nested_func (L112)                          | COVERED |
    |     CoverageVisitor._is_nested_cls (L121)                           | COVERED |
    |     CoverageVisitor._is_private (L133)                              | COVERED |
    |     CoverageVisitor._is_semiprivate (L141)                          | COVERED |
    |     CoverageVisitor._is_ignored_common (L151)                       | COVERED |
    |     CoverageVisitor._has_property_decorators (L168)                 | COVERED |
    |     CoverageVisitor._has_setters (L182)                             | COVERED |
    |     CoverageVisitor._is_func_ignored (L193)                         | COVERED |
    |     CoverageVisitor._is_class_ignored (L217)                        | COVERED |
    |     CoverageVisitor.visit_Module (L221)                             | COVERED |
    |     CoverageVisitor.visit_ClassDef (L228)                           | COVERED |
    |     CoverageVisitor.visit_FunctionDef (L237)                        | COVERED |
    |     CoverageVisitor.visit_AsyncFunctionDef (L246)                   | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/functional/__init__.py (module)                               | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/functional/test_cli.py (module)                               | COVERED |
    |   runner (L22)                                                      | COVERED |
    |   test_run_no_paths (L30)                                           | COVERED |
    |   test_run_shortflags (L77)                                         | COVERED |
    |   test_run_longflags (L106)                                         | COVERED |
    |   test_run_multiple_flags (L124)                                    | COVERED |
    |   test_generate_badge (L135)                                        | COVERED |
    |   test_incompatible_options (L170)                                  | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/functional/test_coverage.py (module)                          | COVERED |
    |   test_coverage_simple (L60)                                        | COVERED |
    |   test_coverage_errors (L73)                                        | COVERED |
    |   test_print_results (L101)                                         | COVERED |
    |   test_print_results_omit_covered (L130)                            | COVERED |
    |   test_print_results_omit_none (L156)                               | COVERED |
    |   test_print_results_omit_all_summary (L174)                        | COVERED |
    |   test_print_results_omit_all_detailed (L198)                       | COVERED |
    |   test_print_results_ignore_module (L226)                           | COVERED |
    |   test_print_results_single_file (L253)                             | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/__init__.py (module)                                     | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/test_badge_gen.py (module)                               | COVERED |
    |   test_save_badge (L26)                                             | COVERED |
    |   test_save_badge_windows (L50)                                     | COVERED |
    |   test_save_badge_no_cairo (L62)                                    | COVERED |
    |   test_get_badge (L73)                                              | COVERED |
    |   test_should_generate (L96)                                        | COVERED |
    |   test_get_color (L115)                                             | COVERED |
    |   test_create (L136)                                                | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/test_config.py (module)                                  | COVERED |
    |   test_find_project_root (L29)                                      | COVERED |
    |   test_find_project_config (L48)                                    | COVERED |
    |   test_parse_pyproject_toml (L57)                                   | COVERED |
    |   test_sanitize_list_values (L93)                                   | COVERED |
    |   test_parse_setup_cfg (L98)                                        | COVERED |
    |   test_parse_setup_cfg_raises (L123)                                | COVERED |
    |   test_read_config_file_none (L134)                                 | COVERED |
    |   test_read_config_file (L193)                                      | COVERED |
    |   test_read_config_file_raises (L207)                               | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/test_utils.py (module)                                   | COVERED |
    |   test_parse_regex (L32)                                            | COVERED |
    |   test_smart_open (L39)                                             | COVERED |
    |   test_get_common_base (L69)                                        | COVERED |
    |   test_get_common_base_windows (L100)                               | COVERED |
    |   test_output_formatter_should_markup (L132)                        | COVERED |
    |   test_output_formatter_set_detailed_markup (L163)                  | COVERED |
    |   test_output_formatter_set_summary_markup (L206)                   | COVERED |
    |   test_output_formatter_interrogate_line_formatter (L258)           | COVERED |
    |   test_output_formatter_interrogate_line_formatter_windows (L319)   | COVERED |
    |   test_output_formatter_get_table_formatter (L343)                  | COVERED |
    |   test_output_formatter_get_table_formatter_py38 (L381)             | COVERED |
    |   test_output_formatter_get_table_formatter_raises (L395)           | COVERED |
    |---------------------------------------------------------------------|---------|

    ------------------------------------ Summary ------------------------------------
    | Name                                  |   Total |   Miss |   Cover |   Cover% |
    |---------------------------------------|---------|--------|---------|----------|
    | src/interrogate/__init__.py           |       1 |      0 |       1 |     100% |
    | src/interrogate/__main__.py           |       1 |      0 |       1 |     100% |
    | src/interrogate/badge_gen.py          |       6 |      0 |       6 |     100% |
    | src/interrogate/cli.py                |       2 |      0 |       2 |     100% |
    | src/interrogate/config.py             |       8 |      0 |       8 |     100% |
    | src/interrogate/coverage.py           |      27 |      0 |      27 |     100% |
    | src/interrogate/utils.py              |      10 |      0 |      10 |     100% |
    | src/interrogate/visit.py              |      18 |      0 |      18 |     100% |
    | tests/functional/__init__.py          |       1 |      0 |       1 |     100% |
    | tests/functional/test_cli.py          |       8 |      0 |       8 |     100% |
    | tests/functional/test_coverage.py     |      10 |      0 |      10 |     100% |
    | tests/unit/__init__.py                |       1 |      0 |       1 |     100% |
    | tests/unit/test_badge_gen.py          |       8 |      0 |       8 |     100% |
    | tests/unit/test_config.py             |      10 |      0 |      10 |     100% |
    | tests/unit/test_utils.py              |      13 |      0 |      13 |     100% |
    |---------------------------------------|---------|--------|---------|----------|
    | TOTAL                                 |     124 |      0 |     124 |   100.0% |
    ---------------- RESULT: PASSED (minimum: 80.0%, actual: 100.0%) ----------------

Other Usage
===========

Generate a `shields.io <https://shields.io/>`_ badge (like this one! |interrogate-badge| ):

.. code-block:: console

    $ interrogate --generate-badge PATH
    RESULT: PASSED (minimum: 80.0%, actual: 100.0%)
    Generated badge to /Users/lynn/dev/interrogate/docs/_static/interrogate_badge.svg

`See below <#badge-options>`_ for more badge configuration.

Add it to your ``tox.ini`` file to enforce a level of coverage:

.. code-block:: ini

    [testenv:doc]
    deps = interrogate
    skip_install = true
    commands =
        interrogate --quiet --fail-under 95 src tests

Or use it with `pre-commit <https://pre-commit.com/>`_:

.. code-block:: yaml

    repos:
      - repo: https://github.com/econchick/interrogate
        rev: 1.7.0  # or master if you're bold
        hooks:
          - id: interrogate
            args: [--quiet, --fail-under=95]
            pass_filenames: false  # needed if excluding files with pyproject.toml or setup.cfg

Use it within your code directly:

.. code-block:: pycon

    >>> from interrogate import coverage
    >>> cov = coverage.InterrogateCoverage(paths=["src"])
    >>> results = cov.get_coverage()
    >>> results
    InterrogateResults(total=68, covered=65, missing=3)


Use ``interrogate`` with `GitHub Actions <https://github.com/features/actions>`_. Check out the `action <https://github.com/marketplace/actions/python-interrogate-check>`_ written & maintained by `Jack McKew <https://github.com/JackMcKew>`_ (thank you, Jack!).

Or use ``interrogate`` in VSCode with the `interrogate extension <https://marketplace.visualstudio.com/items?itemName=kennethlove.interrogate>`_ written & maintained by `Kenneth Love <https://thekennethlove.com/>`_ (thank you, Kenneth!).

Configuration
=============

Configure within your ``pyproject.toml`` (``interrogate`` will automatically detect a ``pyproject.toml`` file and pick up default values for the command line options):

.. code-block:: console

    $ interrogate -c pyproject.toml [OPTIONS] [PATHS]...

.. code-block:: toml

    [tool.interrogate]
    ignore-init-method = false
    ignore-init-module = false
    ignore-magic = false
    ignore-semiprivate = false
    ignore-private = false
    ignore-property-decorators = false
    ignore-module = false
    ignore-nested-functions = false
    ignore-nested-classes = false
    ignore-setters = false
    ignore-overloaded-functions = false
    fail-under = 80
    # example values
    exclude = ["setup.py", "docs", "build"]
    # example regex
    ignore-regex = ["^get$", "^mock_.*", ".*BaseClass.*"]
    ext = []
    # possible values: sphinx (default), google
    style = "sphinx"
    # possible values: 0 (minimal output), 1 (-v), 2 (-vv)
    verbose = 0
    quiet = false
    whitelist-regex = []
    color = true
    omit-covered-files = false
    # output file logation
    generate-badge = "."
    badge-format = "svg"


Or configure within your ``setup.cfg`` (``interrogate`` will automatically detect a ``setup.cfg`` file and pick up default values for the command line options):

.. code-block:: console

    $ interrogate -c setup.cfg [OPTIONS] [PATHS]...

.. code-block:: ini

    [tool:interrogate]
    ignore-init-method = false
    ignore-init-module = false
    ignore-magic = false
    ignore-semiprivate = false
    ignore-private = false
    ignore-property-decorators = false
    ignore-module = false
    ignore-nested-functions = false
    ignore-nested-classes = false
    ignore-setters = false
    ignore-overloaded-functions = false
    fail-under = 80
    ; example values
    exclude = setup.py,docs,build
    ; example regex
    ignore-regex = ^get$,^mock_.*,.*BaseClass.*
    ext = []
    ; possible values: sphinx (default), google
    style = sphinx
    ; possible values: 0 (minimal output), 1 (-v), 2 (-vv)
    verbose = 0
    quiet = false
    whitelist-regex =
    color = true
    omit-covered-files = false
    ; output file logation
    generate-badge = .
    badge-format = svg


.. warning::

    The use of ``setup.cfg`` is not recommended unless for very simple use cases. ``.cfg`` files use a different parser than ``pyproject.toml`` which might cause hard to track down problems. When possible, it is recommended to use ``pyproject.toml`` to define your interrogate configuration.

.. _badge-opts:

Badge Options
=============

Badge Format
------------

The default file format is ``svg``. Use the ``--badge-format`` flag to create a ``png`` file instead.
**Note**: ``interrogate`` must be installed with ``interrogate[png]`` in order to generate ``png`` files (see `above <#extras>`_).

.. code-block:: console

    $ interrogate --generate-badge PATH --badge-format png
    RESULT: PASSED (minimum: 80.0%, actual: 100.0%)
    Generated badge to /Users/lynn/dev/interrogate/docs/_static/interrogate_badge.png

Badge Style
-----------

The following badge styles are available via the ``--badge-style`` flag:

+------------------------------------+--------------------------------+
| option                             | example                        |
+====================================+================================+
| ``flat``                           | |flat-example|                 |
+------------------------------------+--------------------------------+
| ``flat-square``                    | |flat-square-example|          |
+------------------------------------+--------------------------------+
| ``flat-square-modified`` (default) | |interrogate-badge|            |
+------------------------------------+--------------------------------+
| ``for-the-badge``                  | |for-the-badge-example|        |
+------------------------------------+--------------------------------+
| ``plastic``                        | |plastic-example|              |
+------------------------------------+--------------------------------+
| ``social``                         | |social-example|               |
+------------------------------------+--------------------------------+

.. end-readme

Command Line Options
====================

To view all options available, run ``interrogate --help``:

.. code-block:: console

    interrogate -h
    Usage: interrogate [OPTIONS] [PATHS]...

      Measure and report on documentation coverage in Python modules.

    Options:
      --version                       Show the version and exit.
      -v, --verbose                   Level of verbosity.

                                      NOTE: When configuring verbosity in
                                      pyproject.toml or setup.cfg, `verbose=1`
                                      maps to `-v`, and `verbose=2` maps to `-vv`.
                                      `verbose=0` is the equivalent of no verbose
                                      flags used, producing minimal output.
      -q, --quiet                     Do not print output  [default: False]
      -f, --fail-under INT | FLOAT    Fail when coverage % is less than a given
                                      amount.  [default: 80.0]

      -e, --exclude PATH              Exclude PATHs of files and/or directories.
                                      Multiple `-e/--exclude` invocations
                                      supported.

      -i, --ignore-init-method        Ignore `__init__` method of classes.
                                      [default: False]

      -I, --ignore-init-module        Ignore `__init__.py` modules.  [default:
                                      False]

      -m, --ignore-magic              Ignore all magic methods of classes.
                                      [default: False]

                                      NOTE: This does not include the `__init__`
                                      method. To ignore `__init__` methods, use
                                      `--ignore-init-method`.

      -M, --ignore-module             Ignore module-level docstrings.  [default:
                                      False]

      -n, --ignore-nested-functions   Ignore nested functions and methods.
                                      [default: False]

      -C, --ignore-nested-classes     Ignore nested classes.  [default: False]

      -O, --ignore-overloaded-functions
                                      Ignore `@typing.overload`-decorated functions.
                                      [default: False]

      -p, --ignore-private            Ignore private classes, methods, and
                                      functions starting with two underscores.
                                      [default: False]

                                      NOTE: This does not include magic methods;
                                      use `--ignore-magic` and/or `--ignore-init-
                                      method` instead.

      -P, --ignore-property-decorators
                                      Ignore methods with property setter/getter/deleter
                                      decorators.  [default: False]

      -S, --ignore-setters            Ignore methods with property setter
                                      decorators.  [default: False]

      -s, --ignore-semiprivate        Ignore semiprivate classes, methods, and
                                      functions starting with a single underscore.
                                      [default: False]

      -r, --ignore-regex STR          Regex identifying class, method, and
                                      function names to ignore. Multiple
                                      `-r/--ignore-regex` invocations supported.

      --ext                           Include Python-like files with the given
                                      extension (supported: ``pyi``). Multiple
                                      `--ext` invocations supported.

      -w, --whitelist-regex STR       Regex identifying class, method, and
                                      function names to include. Multiple
                                      `-w/--whitelist-regex` invocations
                                      supported.

      --style [sphinx|google]         Style of docstrings to honor. Using `google`
                                      will consider a class and its `__init__`
                                      method both covered if there is either a
                                      class-level docstring, or an `__init__`
                                      method docstring, instead of enforcing both.
                                      Mutually exclusive with `-i`/`--ignore-init`
                                      flag.  [default: sphinx]

      -o, --output FILE               Write output to a given FILE.  [default:
                                      stdout]

      --color / --no-color            Toggle color output on/off when printing to
                                      stdout.  [default: True]

      --omit-covered-files            Omit reporting files that have 100%
                                      documentation coverage. This option is
                                      ignored if verbosity is not set.  [default:
                                      False]

      -g, --generate-badge PATH       Generate a 'shields.io' status badge (an SVG
                                      image) in at a given file or directory. Will
                                      not generate a badge if results did not
                                      change from an existing badge of the same
                                      path.

      --badge-format [svg|png]        File format for the generated badge. Used
                                      with the `-g/--generate-badge` flag.
                                      [default: svg]

                                      NOTE: To generate a PNG file, interrogate
                                      must be installed with `interrogate[png]`,
                                      i.e. `pip install interrogate[png]`.

      --badge-style [flat|flat-square|flat-square-modified|for-the-badge|plastic|social]
                                      Desired style of shields.io badge. Used with
                                      the `-g/--generate-badge` flag. [default:
                                      flat-square-modified]

      -h, --help                      Show this message and exit.
      -c, --config FILE               Read configuration from `pyproject.toml` or
                                      `setup.cfg`.


.. start-uses-this

Users of Interrogate
====================

* `attrs <https://github.com/python-attrs/attrs>`_
* `OpenMMLab <https://github.com/open-mmlab>`_'s ecosystem
* `pyjanitor <https://github.com/ericmjl/pyjanitor>`_
* `klio <https://github.com/spotify/klio>`_

Interrogate in the Wild
-----------------------

* `Why You Should Document Your Tests <https://hynek.me/articles/document-your-tests/>`_ by `Hynek Schlawack <https://twitter.com/hynek>`_
* `Episode #181: It's time to interrogate your Python code <https://pythonbytes.fm/episodes/show/181/it-s-time-to-interrogate-your-python-code>`_ - `PythonBytes podcast <https://pythonbytes.fm/>`_

.. end-uses-this

.. start-credits

Credits
=======

.. role:: smol

``interrogate`` was inspired by |docstr-coverage|_, which was forked from Alexey "DataGreed" Strelkov's |docstring-coverage|_, which was inspired by a 2004 `recipe from James Harlow <http://code.activestate.com/recipes/355731/>`_ :smol:`(turtles...)`.

The cute |sloth| logo is by `JustineW <https://thenounproject.com/wojcik.justine/>`_ purchased via `the Noun Project <https://thenounproject.com/>`_ (but also available under the `Creative Commons License <https://creativecommons.org/licenses/by/3.0/us/legalcode>`_ with attribution).


.. |interrogate-badge|  image:: https://interrogate.readthedocs.io/en/latest/_static/interrogate_badge.svg
.. |flat-example| image:: https://interrogate.readthedocs.io/en/latest/_static/badge_examples/interrogate_badge_f.svg
.. |flat-square-example| image:: https://interrogate.readthedocs.io/en/latest/_static/badge_examples/interrogate_badge_fs.svg
.. |for-the-badge-example| image:: https://interrogate.readthedocs.io/en/latest/_static/badge_examples/interrogate_badge_ftb.svg
.. |plastic-example| image:: https://interrogate.readthedocs.io/en/latest/_static/badge_examples/interrogate_badge_p.svg
.. |social-example| image:: https://interrogate.readthedocs.io/en/latest/_static/badge_examples/interrogate_badge_s.svg
.. |sloth| image:: https://interrogate.readthedocs.io/en/latest/_static/logo_smol.png

.. |docstr-coverage| replace:: ``docstr-coverage``
.. _docstr-coverage: https://pypi.org/project/docstr-coverage
.. |docstring-coverage| replace:: ``docstring-coverage``
.. _docstring-coverage: https://bitbucket.org/DataGreed/docstring-coverage

.. end-credits
