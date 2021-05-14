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

``interrogate`` supports Python 3.6 and above.


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
* on macOS, install ``cairo`` and ``libffi`` (with Homebrew for example);
* on Linux, install the ``cairo``, ``python3-dev`` and ``libffi-dev`` packages (names may vary depending on distribution).

Refer to the ``cairosvg`` `documentation <https://cairosvg.org/documentation/>`_ for more information.

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
    | src/interrogate/badge_gen.py          |       5 |      0 |       5 |     100% |
    | src/interrogate/cli.py                |       2 |      0 |       2 |     100% |
    | src/interrogate/config.py             |       8 |      0 |       8 |     100% |
    | src/interrogate/coverage.py           |      25 |      0 |      25 |     100% |
    | src/interrogate/utils.py              |      10 |      0 |      10 |     100% |
    | src/interrogate/visit.py              |      16 |      0 |      16 |     100% |
    | tests/functional/__init__.py          |       1 |      0 |       1 |     100% |
    | tests/functional/test_cli.py          |       7 |      0 |       7 |     100% |
    | tests/functional/test_coverage.py     |       6 |      0 |       6 |     100% |
    | tests/unit/__init__.py                |       1 |      0 |       1 |     100% |
    | tests/unit/test_badge_gen.py          |       6 |      0 |       6 |     100% |
    | tests/unit/test_config.py             |      10 |      0 |      10 |     100% |
    | tests/unit/test_utils.py              |      13 |      0 |      13 |     100% |
    |---------------------------------------|---------|--------|---------|----------|
    | TOTAL                                 |     112 |      0 |     112 |   100.0% |
    ---------------- RESULT: PASSED (minimum: 95.0%, actual: 100.0%) ----------------


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
    |   save_badge (L33)                                                  | COVERED |
    |   get_badge (L50)                                                   | COVERED |
    |   get_color (L66)                                                   | COVERED |
    |   create (L79)                                                      | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/cli.py (module)                                     | COVERED |
    |   main (L218)                                                       | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/config.py (module)                                  | COVERED |
    |   InterrogateConfig (L17)                                           | COVERED |
    |   find_project_root (L52)                                           | COVERED |
    |   find_project_config (L80)                                         | COVERED |
    |   parse_pyproject_toml (L91)                                        | COVERED |
    |   sanitize_list_values (L107)                                       | COVERED |
    |   parse_setup_cfg (L130)                                            | COVERED |
    |   read_config_file (L164)                                           | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/coverage.py (module)                                | COVERED |
    |   BaseInterrogateResult (L21)                                       | COVERED |
    |     BaseInterrogateResult.perc_covered (L35)                        | COVERED |
    |   InterrogateFileResult (L49)                                       | COVERED |
    |     InterrogateFileResult.combine (L62)                             | COVERED |
    |   InterrogateResults (L76)                                          | COVERED |
    |     InterrogateResults.combine (L88)                                | COVERED |
    |   InterrogateCoverage (L96)                                         | COVERED |
    |     InterrogateCoverage._add_common_exclude (L115)                  | COVERED |
    |     InterrogateCoverage._filter_files (L122)                        | COVERED |
    |     InterrogateCoverage.get_filenames_from_paths (L139)             | COVERED |
    |     InterrogateCoverage._filter_nodes (L166)                        | COVERED |
    |     InterrogateCoverage._get_file_coverage (L192)                   | COVERED |
    |     InterrogateCoverage._get_coverage (L218)                        | COVERED |
    |     InterrogateCoverage.get_coverage (L235)                         | COVERED |
    |     InterrogateCoverage._get_filename (L240)                        | COVERED |
    |     InterrogateCoverage._get_detailed_row (L251)                    | COVERED |
    |     InterrogateCoverage._create_detailed_table (L268)               | COVERED |
    |       InterrogateCoverage._create_detailed_table._sort_nodes (L275) | COVERED |
    |     InterrogateCoverage._print_detailed_table (L297)                | COVERED |
    |     InterrogateCoverage._create_summary_table (L315)                | COVERED |
    |     InterrogateCoverage._print_summary_table (L349)                 | COVERED |
    |     InterrogateCoverage._sort_results (L367)                        | COVERED |
    |     InterrogateCoverage._get_header_base (L397)                     | COVERED |
    |     InterrogateCoverage.print_results (L406)                        | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/utils.py (module)                                   | COVERED |
    |   parse_regex (L22)                                                 | COVERED |
    |   smart_open (L41)                                                  | COVERED |
    |   get_common_base (L61)                                             | COVERED |
    |   OutputFormatter (L81)                                             | COVERED |
    |     OutputFormatter.should_markup (L91)                             | COVERED |
    |     OutputFormatter.set_detailed_markup (L106)                      | COVERED |
    |     OutputFormatter.set_summary_markup (L130)                       | COVERED |
    |     OutputFormatter._interrogate_line_formatter (L159)              | COVERED |
    |     OutputFormatter.get_table_formatter (L222)                      | COVERED |
    |---------------------------------------------------------------------|---------|
    | src/interrogate/visit.py (module)                                   | COVERED |
    |   CovNode (L15)                                                     | COVERED |
    |   CoverageVisitor (L42)                                             | COVERED |
    |     CoverageVisitor._has_doc (L56)                                  | COVERED |
    |     CoverageVisitor._visit_helper (L63)                             | COVERED |
    |     CoverageVisitor._is_nested (L109)                               | COVERED |
    |     CoverageVisitor._is_private (L118)                              | COVERED |
    |     CoverageVisitor._is_semiprivate (L126)                          | COVERED |
    |     CoverageVisitor._is_ignored_common (L136)                       | COVERED |
    |     CoverageVisitor._has_property_decorators (L153)                 | COVERED |
    |     CoverageVisitor._is_func_ignored (L167)                         | COVERED |
    |     CoverageVisitor._is_class_ignored (L188)                        | COVERED |
    |     CoverageVisitor.visit_Module (L192)                             | COVERED |
    |     CoverageVisitor.visit_ClassDef (L199)                           | COVERED |
    |     CoverageVisitor.visit_FunctionDef (L208)                        | COVERED |
    |     CoverageVisitor.visit_AsyncFunctionDef (L217)                   | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/functional/__init__.py (module)                               | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/functional/test_cli.py (module)                               | COVERED |
    |   runner (L22)                                                      | COVERED |
    |   test_run_no_paths (L30)                                           | COVERED |
    |   test_run_shortflags (L71)                                         | COVERED |
    |   test_run_longflags (L97)                                          | COVERED |
    |   test_run_multiple_flags (L115)                                    | COVERED |
    |   test_generate_badge (L126)                                        | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/functional/test_coverage.py (module)                          | COVERED |
    |   test_coverage_simple (L42)                                        | COVERED |
    |   test_coverage_errors (L55)                                        | COVERED |
    |   test_print_results (L83)                                          | COVERED |
    |   test_print_results_ignore_module (L117)                           | COVERED |
    |   test_print_results_single_file (L144)                             | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/__init__.py (module)                                     | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/test_badge_gen.py (module)                               | COVERED |
    |   test_save_badge (L25)                                             | COVERED |
    |   test_save_badge_windows (L47)                                     | COVERED |
    |   test_get_badge (L61)                                              | COVERED |
    |   test_get_color (L85)                                              | COVERED |
    |   test_create (L102)                                                | COVERED |
    |---------------------------------------------------------------------|---------|
    | tests/unit/test_config.py (module)                                  | COVERED |
    |   test_find_project_root (L29)                                      | COVERED |
    |   test_find_project_config (L45)                                    | COVERED |
    |   test_parse_pyproject_toml (L54)                                   | COVERED |
    |   test_sanitize_list_values (L84)                                   | COVERED |
    |   test_parse_setup_cfg (L89)                                        | COVERED |
    |   test_parse_setup_cfg_raises (L114)                                | COVERED |
    |   test_read_config_file_none (L125)                                 | COVERED |
    |   test_read_config_file (L184)                                      | COVERED |
    |   test_read_config_file_raises (L198)                               | COVERED |
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
    | src/interrogate/badge_gen.py          |       5 |      0 |       5 |     100% |
    | src/interrogate/cli.py                |       2 |      0 |       2 |     100% |
    | src/interrogate/config.py             |       8 |      0 |       8 |     100% |
    | src/interrogate/coverage.py           |      25 |      0 |      25 |     100% |
    | src/interrogate/utils.py              |      10 |      0 |      10 |     100% |
    | src/interrogate/visit.py              |      16 |      0 |      16 |     100% |
    | tests/functional/__init__.py          |       1 |      0 |       1 |     100% |
    | tests/functional/test_cli.py          |       7 |      0 |       7 |     100% |
    | tests/functional/test_coverage.py     |       6 |      0 |       6 |     100% |
    | tests/unit/__init__.py                |       1 |      0 |       1 |     100% |
    | tests/unit/test_badge_gen.py          |       6 |      0 |       6 |     100% |
    | tests/unit/test_config.py             |      10 |      0 |      10 |     100% |
    | tests/unit/test_utils.py              |      13 |      0 |      13 |     100% |
    |---------------------------------------|---------|--------|---------|----------|
    | TOTAL                                 |     112 |      0 |     112 |   100.0% |
    ---------------- RESULT: PASSED (minimum: 95.0%, actual: 100.0%) ----------------

Other Usage
===========

Generate a `shields.io <https://shields.io/>`_ badge (like this one! |interrogate-badge| ):

.. code-block:: console

    $ interrogate --generate-badge PATH
    RESULT: PASSED (minimum: 95.0%, actual: 100.0%)
    Generated badge to /Users/lynn/dev/interrogate/docs/_static/interrogate_badge.svg

The default file format is ``svg``. Use the ``--badge-format`` flag to create a ``png`` file instead.
**Note**: ``interrogate`` must be installed with ``interrogate[png]`` in order to generate ``png`` files (see `above <#extras>`_).

.. code-block:: console

    $ interrogate --generate-badge PATH --badge-format png
    RESULT: PASSED (minimum: 95.0%, actual: 100.0%)
    Generated badge to /Users/lynn/dev/interrogate/docs/_static/interrogate_badge.png


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
        rev: 1.4.0  # or master if you're bold
        hooks:
          - id: interrogate
            args: [--quiet, --fail-under=95]

Use it within your code directly:

.. code-block:: pycon

    >>> from interrogate import coverage
    >>> cov = coverage.InterrogateCoverage(paths=["src"])
    >>> results = cov.get_coverage()
    >>> results
    InterrogateResults(total=68, covered=65, missing=3)


Use ``interrogate`` with `GitHub Actions <https://github.com/features/actions>`_. Check out the `action <https://github.com/marketplace/actions/python-interrogate-check>`_ written & maintained by `Jack McKew <https://github.com/JackMcKew>`_ (thank you, Jack!).


Configuration
=============

Configure within your ``pyproject.toml`` (``interrogate`` will automatically detect a ``pyproject.toml`` file and pick up default values for the command line options):

.. code-block:: console

    $ interrogate -c pyproject.toml [OPTIONS] [PATHS]...

.. code-block:: toml

    [tool.interrogate]
    ignore-init-method = true
    ignore-init-module = false
    ignore-magic = false
    ignore-semiprivate = false
    ignore-private = false
    ignore-property-decorators = false
    ignore-module = false
    ignore-nested-functions = false
    ignore-nested-classes = true
    ignore-setters = false
    fail-under = 95
    exclude = ["setup.py", "docs", "build"]
    ignore-regex = ["^get$", "^mock_.*", ".*BaseClass.*"]
    verbose = 0
    quiet = false
    whitelist-regex = []
    color = true
    generate-badge = "."
    badge-format = "svg"


Or configure within your ``setup.cfg`` (``interrogate`` will automatically detect a ``setup.cfg`` file and pick up default values for the command line options):

.. code-block:: console

    $ interrogate -c setup.cfg [OPTIONS] [PATHS]...

.. code-block:: ini

    [tool:interrogate]
    ignore-init-method = true
    ignore-init-module = false
    ignore-magic = false
    ignore-semiprivate = false
    ignore-private = false
    ignore-property-decorators = false
    ignore-module = false
    ignore-nested-functions = false
    ignore-nested-classes = true
    ignore-setters = false
    fail-under = 95
    exclude = setup.py,docs,build
    ignore-regex = ^get$,^mock_.*,.*BaseClass.*
    verbose = 0
    quiet = false
    whitelist-regex =
    color = true
    generate-badge = .
    badge-format = svg


.. warning::

    The use of ``setup.cfg`` is not recommended unless for very simple use cases. ``.cfg`` files use a different parser than ``pyproject.toml`` which might cause hard to track down problems. When possible, it is recommended to use ``pyproject.toml`` to define your interrogate configuration.


.. end-readme

To view all options available, run ``interrogate --help``:

.. code-block:: console

    interrogate -h
    Usage: interrogate [OPTIONS] [PATHS]...

      Measure and report on documentation coverage in Python modules.

    Options:
      --version                       Show the version and exit.
      -v, --verbose                   Level of verbosity  [default: 0]
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

      -p, --ignore-private            Ignore private classes, methods, and
                                      functions starting with two underscores.
                                      [default: False]

                                      NOTE: This does not include magic methods;
                                      use `--ignore-magic` and/or `--ignore-init-
                                      method` instead.

      -P, --ignore-property-decorators
                                      Ignore methods with property setter/getter
                                      decorators.  [default: False]

      -S, --ignore-setters            Ignore methods with property setter
                                      decorators.  [default: False]

      -s, --ignore-semiprivate        Ignore semiprivate classes, methods, and
                                      functions starting with a single underscore.
                                      [default: False]

      -r, --ignore-regex STR          Regex identifying class, method, and
                                      function names to ignore. Multiple
                                      `-r/--ignore-regex` invocations supported.

      -w, --whitelist-regex STR       Regex identifying class, method, and
                                      function names to include. Multiple
                                      `-w/--whitelist-regex` invocations
                                      supported.

      -o, --output FILE               Write output to a given FILE.  [default:
                                      stdout]

      --color / --no-color            Toggle color output on/off when printing to
                                      stdout.  [default: True]

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

      -h, --help                      Show this message and exit.
      -c, --config FILE               Read configuration from `pyproject.toml` or
                                      `setup.cfg`.

.. start-credits

Credits
=======

.. role:: smol

``interrogate`` was inspired by |docstr-coverage|_, which was forked from Alexey "DataGreed" Strelkov's |docstring-coverage|_, which was inspired by a 2004 `recipe from James Harlow <http://code.activestate.com/recipes/355731/>`_ :smol:`(turtles...)`.

The cute |sloth| logo is by `JustineW <https://thenounproject.com/wojcik.justine/>`_ purchased via `the Noun Project <https://thenounproject.com/>`_ (but also available under the `Creative Commons License <https://creativecommons.org/licenses/by/3.0/us/legalcode>`_ with attribution).


.. |interrogate-badge|  image:: https://interrogate.readthedocs.io/en/latest/_static/interrogate_badge.svg
.. |sloth| image:: https://interrogate.readthedocs.io/en/latest/_static/logo_smol.png

.. |docstr-coverage| replace:: ``docstr-coverage``
.. _docstr-coverage: https://pypi.org/project/docstr-coverage
.. |docstring-coverage| replace:: ``docstring-coverage``
.. _docstring-coverage: https://bitbucket.org/DataGreed/docstring-coverage

.. end-credits
