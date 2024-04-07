=================================
``interrogate``: explain yourself
=================================


.. toctree::
   :maxdepth: 2

   index

.. include:: ../README.rst
   :start-after: start-readme
   :end-before: end-readme


Command Line Options
====================

.. program:: interrogate [OPTIONS] [PATHS]...

.. option:: --version

    Show the version and exit.

.. option:: -v, --verbose

    Level of verbosity.

    NOTE: When configuring verbosity in ``pyproject.toml`` or ``setup.cfg``,
    ``verbose=1`` maps to ``-v``, and ``verbose=2`` maps to ``-vv``.
    ``verbose=0`` is the equivalent of no verbose flags used, producing minimal output.

.. option:: -q, --quiet

    Do not print output  [default: ``False``]

.. option:: -f, --fail-under INT | FLOAT

    Fail when coverage % is less than a given amount.  [default: ``80.0``]

.. option:: -e, --exclude PATH

    Exclude PATHs of files and/or directories. Multiple ``-e/--exclude`` invocations supported.

.. option:: -i, --ignore-init-method

    Ignore ``__init__`` method of classes. [default: ``False``]

.. option:: -I, --ignore-init-module

    Ignore ``__init__.py`` modules.  [default: ``False``]

.. option:: -m, --ignore-magic

    Ignore all magic methods of classes.  [default: ``False``]

    NOTE: This does not include the ``__init__`` method. To ignore ``__init__`` methods, use ``--ignore-init-method``.

.. option:: -M, --ignore-module

    Ignore module-level docstrings.  [default: ``False``]

.. option:: -n, --ignore-nested-functions

    Ignore nested functions and methods.  [default: ``False``]

.. option:: -C, --ignore-nested-classes

    Ignore nested classes.  [default: ``False``]

.. option:: -O, --ignore-overloaded-functions

    Ignore `@typing.overload`-decorated functions.  [default: ``False``]

.. option:: -p, --ignore-private

    Ignore private classes, methods, and functions starting with two underscores.  [default: ``False``]

    NOTE: This does not include magic methods; use ``--ignore-magic`` and/or ``--ignore-init-method`` instead.

.. option:: -P, --ignore-property-decorators

    Ignore methods with property setter/getter/deleter decorators.  [default: ``False``]

.. option:: -S, --ignore-setters

    Ignore methods with property setter decorators.  [default: ``False``]

.. option:: -s, --ignore-semiprivate

    Ignore semiprivate classes, methods, and functions starting with a single underscore. [default: ``False``]

.. option:: -r, --ignore-regex STR

    Regex identifying class, method, and function names to ignore. Multiple ``-r/--ignore-regex`` invocations supported.

.. option:: --ext STR

    Include Python-like files with the given extension (supported: ``pyi``). Multiple ``--ext`` invocations supported.

.. option:: -w, --whitelist-regex STR

    Regex identifying class, method, and function names to include. Multiple ``-r/--ignore-regex`` invocations supported.

.. option:: --style [sphinx|google]

    Style of docstrings to honor. Using ``google`` will consider a class and its ``__init__`` method
    both covered if there is either a class-level docstring, or an ``__init__`` method docstring,
    instead of enforcing both. Mutually exclusive with ``-i/--ignore-init`` flag.
    [default: ``sphinx``]

.. option:: -o, --output FILE

    Write output to a given ``FILE``.  [default: ``stdout``]

.. option:: -c, --config FILE

    Read configuration from ``pyproject.toml`` or ``setup.cfg``.

.. option:: --color, --no-color

    Toggle color output on/off when printing to stdout.  [default: color]

.. option:: --omit-covered-files

    Omit reporting files that have 100% documentation coverage.
    This option is ignored if verbosity is not set.  [default: ``False``]

.. option:: -g, --generate-badge PATH

    Generate a `shields.io <https://shields.io/>`_ status badge (an SVG image) in at a given file
    or directory. Will not generate a badge if results did not change from an existing badge of
    the same path.

.. option:: --badge-format [svg|png]

    File format for the generated badge. Used with the ``-g/--generate-badge`` flag.  [default: ``svg``]

    NOTE: To generate a PNG file, interrogate must be installed with ``interrogate[png]``, i.e.
    ``pip install interrogate[png]``.

.. option:: --badge-style [flat|flat-square|flat-square-modified|for-the-badge|plastic|social]

    Desired style of `shields.io <https://shields.io/>`_ badge.
    Used with the `-g/--generate-badge` flag. [default: flat-square-modified]


.. include:: ../README.rst
   :start-after: start-uses-this
   :end-before: end-uses-this

.. include:: ../README.rst
   :start-after: start-credits
   :end-before: end-credits

.. include:: changelog.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. _pip: https://pip.pypa.io/en/stable/
.. _virtualenv: https://hynek.me/articles/virtualenv-lives/
