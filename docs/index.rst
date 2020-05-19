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

    Level of verbosity  [default: ``0``]

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

.. option:: -p, --ignore-private

    Ignore private classes, methods, and functions starting with two underscores.  [default: ``False``]

    NOTE: This does not include magic methods; use ``--ignore-magic`` and/or ``--ignore-init-method`` instead.

.. option:: -s, --ignore-semiprivate

    Ignore semiprivate classes, methods, and functions starting with a single underscore. [default: ``False``]

.. option:: -r, --ignore-regex STR

    Regex identifying class, method, and function names to ignore. Multiple ``-r/--ignore-regex`` invocations supported.

.. option:: -w, --whitelist-regex STR

    Regex identifying class, method, and function names to include. Multiple ``-r/--ignore-regex`` invocations supported.

.. option:: -o, --output FILE

    Write output to a given ``FILE``.  [default: ``stdout``]

.. option:: -c, --config FILE

    Read configuration from ``pyproject.toml``.

.. option:: --color, --no-color

  Toggle color output on/off when printing to stdout.  [default: color]

.. option:: -g, --generate-badge PATH

    Generate a `shields.io <https://shields.io/>`_ status badge (an SVG image) in at a given file or directory.


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
