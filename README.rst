``interrogate``: explain yourself
=================================

Interrogate a codebase for docstring coverage.

.. start-readme

Requirements
------------

``interrogate`` supports Python 3.5 and above.


Installation
------------

``interrogate`` available on `PyPI <https://pypi.org/project/interrogate/>`_ and `GitHub <https://github.com/econchick/interrogate>`_. The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a `virtualenv <https://hynek.me/articles/virtualenv-lives/>`_:

.. code-block:: console

    $ pip install interrogate

Usage
-----

Try it out on a Python project:

.. code-block:: console

    $ interrogate [PATH]
    RESULT: PASSED (minumum: 80.0%, actual: 100.0%)


Add verbosity to see a summary:

.. code-block:: console

    $ interrogate -v [PATH]

    ============ Coverage for /Users/lynn/dev/interrogate/ ==============
    ------------------------------ Summary ------------------------------
    | Name                          |  Total |  Miss |  Cover |  Cover% |
    |-------------------------------|--------|-------|--------|---------|
    | src/interrogate/__init__.py   |      1 |     0 |      1 |    100% |
    | src/interrogate/cli.py        |      2 |     0 |      2 |    100% |
    | src/interrogate/config.py     |      6 |     0 |      6 |    100% |
    | src/interrogate/coverage.py   |     19 |     0 |     19 |    100% |
    | src/interrogate/utils.py      |      6 |     0 |      6 |    100% |
    | src/interrogate/visit.py      |     14 |     0 |     14 |    100% |
    | tests/functional/test_cli.py  |      5 |     0 |      5 |    100% |
    |-------------------------------|--------|-------|--------|---------|
    | TOTAL                         |     53 |     0 |     53 |  100.0% |
    ---------- RESULT: PASSED (minumum: 80.0%, actual: 100.0%) ----------


Add even *more* verbosity:


.. code-block:: console

    $ interrogate -vv [PATH]

    ============= Coverage for /Users/lynn/dev/interrogate/ =============
    -------------------------- Detailed Coverage ------------------------
    | Name                                                    |  Status |
    |---------------------------------------------------------|---------|
    | src/interrogate/__init__.py (module)                    | COVERED |
    |---------------------------------------------------------|---------|
    | src/interrogate/cli.py (module)                         | COVERED |
    |   main (L15)                                            | COVERED |
    |---------------------------------------------------------|---------|
    | src/interrogate/config.py (module)                      | COVERED |
    |   InterrogateConfig (L14)                               | COVERED |
    |   find_project_root (L28)                               | COVERED |
    |   find_pyproject_toml (L55)                             | COVERED |
    |   parse_pyproject_toml (L62)                            | COVERED |
    |   read_pyproject_toml (L71)                             | COVERED |
    |---------------------------------------------------------|---------|
    | src/interrogate/coverage.py (module)                    | COVERED |
    |   BaseInterrogateResult (L21)                           | COVERED |
    |     BaseInterrogateResult.perc_covered (L30)            | COVERED |
    |   InterrogateFileResult (L38)                           | COVERED |
    |     InterrogateFileResult.combine (L46)                 | COVERED |
    |   InterrogateResults (L61)                              | COVERED |
    |     InterrogateResults.combine (L68)                    | COVERED |
    |   InterrogateCoverage (L77)                             | COVERED |
    |     InterrogateCoverage._add_common_exclude (L89)       | COVERED |
    |     InterrogateCoverage._filter_files (L96)             | COVERED |
    |     InterrogateCoverage.get_filenames_from_paths (L113) | COVERED |
    |     InterrogateCoverage._get_file_coverage (L139)       | COVERED |
    |     InterrogateCoverage.get_coverage (L156)             | COVERED |
    |     InterrogateCoverage._get_detailed_row (L171)        | COVERED |
    |     InterrogateCoverage._create_detailed_table (L185)   | COVERED |
    |     InterrogateCoverage._print_detailed_table (L204)    | COVERED |
    |     InterrogateCoverage._create_summary_table (L216)    | COVERED |
    |     InterrogateCoverage._print_summary_table (L250)     | COVERED |
    |     InterrogateCoverage.print_results (L261)            | COVERED |
    |---------------------------------------------------------|---------|
    | src/interrogate/utils.py (module)                       | COVERED |
    |   parse_regex (L17)                                     | COVERED |
    |   smart_open (L24)                                      | COVERED |
    |   get_common_base (L39)                                 | COVERED |
    |     get_common_base.allnamesequal (L42)                 | COVERED |
    |   interrogate_line_formatter (L51)                      | COVERED |
    |---------------------------------------------------------|---------|
    | src/interrogate/visit.py (module)                       | COVERED |
    |   CovNode (L11)                                         | COVERED |
    |   CoverageVisitor (L23)                                 | COVERED |
    |     CoverageVisitor._has_doc (L33)                      | COVERED |
    |     CoverageVisitor._visit_helper (L41)                 | COVERED |
    |     CoverageVisitor._is_private (L83)                   | COVERED |
    |     CoverageVisitor._is_semiprivate (L91)               | COVERED |
    |     CoverageVisitor._is_ignored_common (L101)           | COVERED |
    |     CoverageVisitor._is_func_ignored (L117)             | COVERED |
    |     CoverageVisitor._is_class_ignored (L134)            | COVERED |
    |     CoverageVisitor.visit_Module (L138)                 | COVERED |
    |     CoverageVisitor.visit_ClassDef (L142)               | COVERED |
    |     CoverageVisitor.visit_FunctionDef (L149)            | COVERED |
    |     CoverageVisitor.visit_AsyncFunctionDef (L156)       | COVERED |
    |---------------------------------------------------------|---------|
    | tests/functional/test_cli.py (module)                   | COVERED |
    |   runner (L16)                                          | COVERED |
    |   test_run_shortflags (L22)                             | COVERED |
    |   test_run_longflags (L57)                              | COVERED |
    |   test_run_multiple_flags (L81)                         | COVERED |
    |---------------------------------------------------------|---------|

    ------------------------------ Summary ------------------------------
    | Name                          |  Total |  Miss |  Cover |  Cover% |
    |-------------------------------|--------|-------|--------|---------|
    | src/interrogate/__init__.py   |      1 |     0 |      1 |    100% |
    | src/interrogate/cli.py        |      2 |     0 |      2 |    100% |
    | src/interrogate/config.py     |      6 |     0 |      6 |    100% |
    | src/interrogate/coverage.py   |     19 |     0 |     19 |    100% |
    | src/interrogate/utils.py      |      6 |     0 |      6 |    100% |
    | src/interrogate/visit.py      |     14 |     0 |     14 |    100% |
    | tests/functional/test_cli.py  |      5 |     0 |      5 |    100% |
    |-------------------------------|--------|-------|--------|---------|
    | TOTAL                         |     53 |     0 |     53 |  100.0% |
    ---------- RESULT: PASSED (minumum: 80.0%, actual: 100.0%) ----------


Other Usage
-----------

Add it to your ``tox.ini`` file to enforce a level of coverage:

.. code-block:: ini

    [testenv:doc]
    deps = interrogate
    skip_install = true
    commands =
        interrogate --quiet --fail-under 95 src tests


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
    exclude = ["setup.py", "docs"]
    verbose = 0
    quiet = false


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
                                    names to ignore.

      -o, --output FILE             Write output to a given FILE.  [default:
                                    stdout]

      -c, --config FILE             Read configuration from `pyproject.toml`.
      -h, --help                    Show this message and exit.
