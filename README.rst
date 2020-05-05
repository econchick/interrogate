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

``interrogate`` supports Python 3.5 and above.


Installation
============

``interrogate`` available on `PyPI <https://pypi.org/project/interrogate/>`_ and `GitHub <https://github.com/econchick/interrogate>`_. The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a `virtualenv <https://hynek.me/articles/virtualenv-lives/>`_:

.. code-block:: console

    $ pip install interrogate

Usage
=====

Try it out on a Python project:

.. code-block:: console

    $ interrogate [PATH]
    RESULT: PASSED (minimum: 80.0%, actual: 100.0%)


Add verbosity to see a summary:

.. code-block:: console

    $ interrogate -v [PATH]

    ==================== Coverage for /Users/lynn/dev/interrogate/ ======================
    -------------------------------------- Summary --------------------------------------
    | Name                                      |   Total |   Miss |   Cover |   Cover% |
    |-------------------------------------------|---------|--------|---------|----------|
    | tests/unit/__init__.py                    |       1 |      0 |       1 |     100% |
    | tests/unit/test_badge_gen.py              |       5 |      0 |       5 |     100% |
    | tests/unit/test_config.py                 |       7 |      0 |       7 |     100% |
    | tests/unit/test_utils.py                  |       5 |      0 |       5 |     100% |
    | tests/functional/__init__.py              |       1 |      0 |       1 |     100% |
    | tests/functional/test_cli.py              |       7 |      0 |       7 |     100% |
    | tests/functional/test_coverage.py         |       4 |      0 |       4 |     100% |
    | src/interrogate/__init__.py               |       1 |      0 |       1 |     100% |
    | src/interrogate/badge_gen.py              |       5 |      0 |       5 |     100% |
    | src/interrogate/cli.py                    |       2 |      0 |       2 |     100% |
    | src/interrogate/config.py                 |       6 |      0 |       6 |     100% |
    | src/interrogate/coverage.py               |      22 |      0 |      22 |     100% |
    | src/interrogate/utils.py                  |       6 |      0 |       6 |     100% |
    | src/interrogate/visit.py                  |      14 |      0 |      14 |     100% |
    |-------------------------------------------|---------|--------|---------|----------|
    | TOTAL                                     |      86 |      0 |      86 |   100.0% |
    ------------------ RESULT: PASSED (minimum: 80.0%, actual: 100.0%) ------------------


Add even *more* verbosity:


.. code-block:: console

    $ interrogate -vv [PATH]

    ==================== Coverage for /Users/lynn/dev/interrogate/ ======================
    --------------------------------- Detailed Coverage ---------------------------------
    | Name                                                                  |    Status |
    |-----------------------------------------------------------------------|-----------|
    | tests/unit/__init__.py (module)                                       |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | tests/unit/test_badge_gen.py (module)                                 |   COVERED |
    |   test_save_badge (L14)                                               |   COVERED |
    |   test_get_badge (L35)                                                |   COVERED |
    |   test_get_color (L44)                                                |   COVERED |
    |   test_create (L61)                                                   |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | tests/unit/test_config.py (module)                                    |   COVERED |
    |   test_find_project_root (L13)                                        |   COVERED |
    |   test_find_pyproject_toml (L40)                                      |   COVERED |
    |   test_parse_pyproject_toml (L52)                                     |   COVERED |
    |   test_read_pyproject_toml_none (L68)                                 |   COVERED |
    |   test_read_pyproject_toml (L76)                                      |   COVERED |
    |   test_read_pyproject_toml_raises (L106)                              |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | tests/unit/test_utils.py (module)                                     |   COVERED |
    |   test_parse_regex (L12)                                              |   COVERED |
    |   test_smart_open (L21)                                               |   COVERED |
    |   test_get_common_base (L38)                                          |   COVERED |
    |   test_interrogate_line_formatter (L52)                               |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | tests/functional/__init__.py (module)                                 |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | tests/functional/test_cli.py (module)                                 |   COVERED |
    |   runner (L18)                                                        |   COVERED |
    |   test_run_no_paths (L24)                                             |   COVERED |
    |   test_run_shortflags (L34)                                           |   COVERED |
    |   test_run_longflags (L69)                                            |   COVERED |
    |   test_run_multiple_flags (L93)                                       |   COVERED |
    |   test_generate_badge (L111)                                          |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | tests/functional/test_coverage.py (module)                            |   COVERED |
    |   test_coverage_simple (L16)                                          |   COVERED |
    |   test_coverage_errors (L37)                                          |   COVERED |
    |   test_print_results (L57)                                            |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/__init__.py (module)                                  |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/badge_gen.py (module)                                 |   COVERED |
    |   save_badge (L33)                                                    |   COVERED |
    |   get_badge (L50)                                                     |   COVERED |
    |   get_color (L66)                                                     |   COVERED |
    |   create (L79)                                                        |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/cli.py (module)                                       |   COVERED |
    |   main (L16)                                                          |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/config.py (module)                                    |   COVERED |
    |   InterrogateConfig (L14)                                             |   COVERED |
    |   find_project_root (L43)                                             |   COVERED |
    |   find_pyproject_toml (L71)                                           |   COVERED |
    |   parse_pyproject_toml (L78)                                          |   COVERED |
    |   read_pyproject_toml (L94)                                           |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/coverage.py (module)                                  |   COVERED |
    |   BaseInterrogateResult (L21)                                         |   COVERED |
    |     BaseInterrogateResult.perc_covered (L37)                          |   COVERED |
    |   InterrogateFileResult (L51)                                         |   COVERED |
    |     InterrogateFileResult.combine (L65)                               |   COVERED |
    |   InterrogateResults (L80)                                            |   COVERED |
    |     InterrogateResults.combine (L93)                                  |   COVERED |
    |   InterrogateCoverage (L102)                                          |   COVERED |
    |     InterrogateCoverage._add_common_exclude (L120)                    |   COVERED |
    |     InterrogateCoverage._filter_files (L127)                          |   COVERED |
    |     InterrogateCoverage.get_filenames_from_paths (L144)               |   COVERED |
    |     InterrogateCoverage._get_file_coverage (L171)                     |   COVERED |
    |     InterrogateCoverage._get_coverage (L188)                          |   COVERED |
    |     InterrogateCoverage.get_coverage (L203)                           |   COVERED |
    |     InterrogateCoverage._get_detailed_row (L208)                      |   COVERED |
    |     InterrogateCoverage._create_detailed_table (L222)                 |   COVERED |
    |       InterrogateCoverage._create_detailed_table._sort_nodes (L229)   |   COVERED |
    |     InterrogateCoverage._print_detailed_table (L251)                  |   COVERED |
    |     InterrogateCoverage._create_summary_table (L263)                  |   COVERED |
    |     InterrogateCoverage._print_summary_table (L297)                   |   COVERED |
    |     InterrogateCoverage._sort_results (L308)                          |   COVERED |
    |     InterrogateCoverage.print_results (L341)                          |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/utils.py (module)                                     |   COVERED |
    |   parse_regex (L17)                                                   |   COVERED |
    |   smart_open (L32)                                                    |   COVERED |
    |   get_common_base (L53)                                               |   COVERED |
    |     get_common_base.allnamesequal (L65)                               |   COVERED |
    |   interrogate_line_formatter (L74)                                    |   COVERED |
    |-----------------------------------------------------------------------|-----------|
    | src/interrogate/visit.py (module)                                     |   COVERED |
    |   CovNode (L11)                                                       |   COVERED |
    |   CoverageVisitor (L34)                                               |   COVERED |
    |     CoverageVisitor._has_doc (L48)                                    |   COVERED |
    |     CoverageVisitor._visit_helper (L56)                               |   COVERED |
    |     CoverageVisitor._is_private (L95)                                 |   COVERED |
    |     CoverageVisitor._is_semiprivate (L103)                            |   COVERED |
    |     CoverageVisitor._is_ignored_common (L113)                         |   COVERED |
    |     CoverageVisitor._is_func_ignored (L129)                           |   COVERED |
    |     CoverageVisitor._is_class_ignored (L146)                          |   COVERED |
    |     CoverageVisitor.visit_Module (L150)                               |   COVERED |
    |     CoverageVisitor.visit_ClassDef (L157)                             |   COVERED |
    |     CoverageVisitor.visit_FunctionDef (L167)                          |   COVERED |
    |     CoverageVisitor.visit_AsyncFunctionDef (L177)                     |   COVERED |
    |-----------------------------------------------------------------------|-----------|

    -------------------------------------- Summary --------------------------------------
    | Name                                      |   Total |   Miss |   Cover |   Cover% |
    |-------------------------------------------|---------|--------|---------|----------|
    | tests/unit/__init__.py                    |       1 |      0 |       1 |     100% |
    | tests/unit/test_badge_gen.py              |       5 |      0 |       5 |     100% |
    | tests/unit/test_config.py                 |       7 |      0 |       7 |     100% |
    | tests/unit/test_utils.py                  |       5 |      0 |       5 |     100% |
    | tests/functional/__init__.py              |       1 |      0 |       1 |     100% |
    | tests/functional/test_cli.py              |       7 |      0 |       7 |     100% |
    | tests/functional/test_coverage.py         |       4 |      0 |       4 |     100% |
    | src/interrogate/__init__.py               |       1 |      0 |       1 |     100% |
    | src/interrogate/badge_gen.py              |       5 |      0 |       5 |     100% |
    | src/interrogate/cli.py                    |       2 |      0 |       2 |     100% |
    | src/interrogate/config.py                 |       6 |      0 |       6 |     100% |
    | src/interrogate/coverage.py               |      22 |      0 |      22 |     100% |
    | src/interrogate/utils.py                  |       6 |      0 |       6 |     100% |
    | src/interrogate/visit.py                  |      14 |      0 |      14 |     100% |
    |-------------------------------------------|---------|--------|---------|----------|
    | TOTAL                                     |      86 |      0 |      86 |   100.0% |
    ------------------ RESULT: PASSED (minimum: 80.0%, actual: 100.0%) ------------------


Other Usage
===========

Generate a `shields.io <https://shields.io/>`_ badge (like this one! |interrogate-badge| ):

.. code-block:: console

    $ interrogate --generate-badge PATH
    RESULT: PASSED (minimum: 80.0%, actual: 100.0%)
    Generated badge to /Users/lynn/dev/interrogate/docs/_static/interrogate_badge.svg

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
        rev: 1.1.4  # or master if you're bold
        hooks:
          - id: interrogate
            args: [--quiet, --fail-under=95]

Use it within your code directly:

.. code-block:: pycon

    >>> from interrogate import coverage
    >>> cov = coverage.InterrogateCoverage(paths=["src"])
    >>> results = cov.get_coverage()
    >>> results
    InterrogateResults(total=51, covered=48, missing=3, skipped=0)


Configure within your ``pyproject.toml``:

.. code-block:: console

    $ interrogate -c pyproject.toml [OPTIONS] [PATHS]...

.. code-block:: toml

    [tool.interrogate]
    ignore-init-method = true
    ignore-init-module = false
    ignore-magic = false
    ignore-semiprivate = false
    ignore-private = false
    ignore-module = false
    fail-under = 95
    exclude = ["setup.py", "docs", "build"]
    ignore-regex = ["^get$", "^mock_.*", ".*BaseClass.*"]
    verbose = 0
    quiet = false
    whitelist-regex = []


.. end-readme

To view all options available, run ``interrogate --help``:

.. code-block:: console

    interrogate -h
    Usage: interrogate [OPTIONS] [PATHS]...

      Measure and report on documentation coverage in Python modules.

    Options:
      --version                     Show the version and exit.
      -v, --verbose                 Level of verbosity  [default: 0]
      -q, --quiet                   Do not print output  [default: False]
      -f, --fail-under INT | FLOAT  Fail when coverage % is less than a given
                                    amount.  [default: 80.0]

      -e, --exclude PATH            Exclude PATHs of files and/or directories.
                                    Multiple `-e/--exclude` invocations supported.

      -i, --ignore-init-method      Ignore `__init__` method of classes.
                                    [default: False]

      -I, --ignore-init-module      Ignore `__init__.py` modules.  [default:
                                    False]

      -m, --ignore-magic            Ignore all magic methods of classes.
                                    [default: False]

                                    NOTE: This does not include the `__init__`
                                    method. To ignore `__init__` methods, use
                                    `--ignore-init-method`.

      -M, --ignore-module           Ignore module-level docstrings.  [default:
                                    False]

      -p, --ignore-private          Ignore private classes, methods, and functions
                                    starting with two underscores.
                                    [default:False]

                                    NOTE: This does not include magic methods; use
                                    `--ignore-magic` and/or `--ignore-init-method`
                                    instead.

      -s, --ignore-semiprivate      Ignore semiprivate classes, methods, and
                                    functions starting with a single underscore.
                                    [default: False]

      -r, --ignore-regex STR        Regex identifying class, method, and function
                                    names to ignore. Multiple `-r/--ignore-regex`
                                    invocations supported.

      -w, --whitelist-regex STR     Regex identifying class, method, and function
                                    names to include. Multiple `-w/--whitelist-
                                    regex` invocations supported.

      -o, --output FILE             Write output to a given FILE.  [default:
                                    stdout]

      -c, --config FILE             Read configuration from `pyproject.toml`.
      -g, --generate-badge PATH     Generate a 'shields.io' status badge (an SVG
                                    image) in at a given file or directory.
      -h, --help                    Show this message and exit.


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
