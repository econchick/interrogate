Changelog
=========

.. short-log

1.7.0 (2024-04-07)
------------------

Added
^^^^^

* `tomli` dependency for Python versions < 3.11, making use of `tomllib` in the standard library with 3.11+ (`#150 <https://github.com/econchick/interrogate/issues/150>`_).
* Support for ``pyi`` file extensions (and leave room for other file extensions to be added, like maybe ``ipynb``).
* Support for Google-style docstrings for class ``__init__`` methods with new ``--style [sphinx|google]`` flag (`#128 <https://github.com/econchick/interrogate/issues/128>`_).

Fixed
^^^^^

* Include support for deleters when ignoring property decorators (`#126 <https://github.com/econchick/interrogate/issues/126>_`).
* Support floats for `--fail-under` values (`#114 <https://github.com/econchick/interrogate/issues/114>`_).

Removed
^^^^^^^

* `toml` dependency for all Python versions (`#150 <https://github.com/econchick/interrogate/issues/150>`_).

.. short-log

1.6.0 (2024-04-06)
------------------

Added
^^^^^

* Add ``--ignore-overloaded-functions`` flag to ignore overload decorators (`#97 <https://github.com/econchick/interrogate/issues/97>`_) – thank you `ErwinJunge <https://github.com/econchick/interrogate/pull/98>`_ (via `#167 <https://github.com/econchick/interrogate/pull/167>`_) and `zackyancey <https://github.com/econchick/interrogate/pull/160>`_.
* Support for Python 3.11 & 3.12.

Removed
^^^^^^^

* Support for Python 3.6 & 3.7.


1.5.0 (2021-09-10)
------------------

Added
^^^^^

* Set minimum ``click`` version (thank you bildzeitung! `#81 <https://github.com/econchick/interrogate/issues/81>`_, `#82 <https://github.com/econchick/interrogate/pull/82>`_).
* Add ``--omit-covered-files`` flag to skip reporting fully-covered files (`#85 <https://github.com/econchick/interrogate/issues/85>`_).
* Add support for different badge styles via new ``--badge-style`` flag (`#86 <https://github.com/econchick/interrogate/issues/86>`_).
* Add 3.10 support!

Fixed
^^^^^
* Clarify ``verbose`` configuration (`#83 <https://github.com/econchick/interrogate/issues/83>`_).


1.4.0 (2021-05-14)
------------------

Added
^^^^^

* Support for generating the status badge as a PNG file with a new ``--badge-format`` flag (`#70 <https://github.com/econchick/interrogate/issues/70>`_).
* Add new option ``-C`` / ``--ignore-nested-classes`` to ignore – you guessed it – nested classes (`#65 <https://github.com/econchick/interrogate/issues/65>`_).
* Add new option ``-S`` / ``--ignore-setters`` to ignore property setter decorators (`#68 <https://github.com/econchick/interrogate/issues/68>`_).

1.3.2 (2020-11-03)
------------------

Added
^^^^^

* Add wicked cute Sloth logo to status badge (`#48 <https://github.com/econchick/interrogate/issues/48>`_).
* Testing/support for Python 3.9 – thank you `s-weigand <https://github.com/econchick/interrogate/pull/58>`_!

Fixed
^^^^^

* Excluding paths are no longer OS-dependent (`#51 <https://github.com/econchick/interrogate/issues/51>`_) – thank you `oriash93 <https://github.com/econchick/interrogate/pull/56>`_!
* Include Python trove classifiers in packaging (`#61 <https://github.com/econchick/interrogate/issues/61>`_) – thank you `mmtj <https://github.com/econchick/interrogate/pull/62>`_!

Removed
^^^^^^^

* Support for Python 3.5 – thank you `s-weigand <https://github.com/econchick/interrogate/pull/58>`_!


1.3.1 (2020-09-03)
------------------

Fixed
^^^^^

* Only generate a status badge if results have changed from an existing badge (`#40 <https://github.com/econchick/interrogate/issues/40>`_).


1.3.0 (2020-08-23)
------------------

Added
^^^^^

* Read configuration from ``pyproject.toml`` by default (`#36 <https://github.com/econchick/interrogate/issues/36>`_).
* Add ``-P`` / ``--ignore-property-decorators`` flag to ignore methods with property getter/setter decorators (`#37 <https://github.com/econchick/interrogate/issues/37>`_).
* Add support for read configuration from ``setup.cfg`` (`#35 <https://github.com/econchick/interrogate/issues/35>`_).

Fixed
^^^^^
* ``-e`` / ``--exclude`` doesn't error if a non-existent file/directory is passed (`#38 <https://github.com/econchick/interrogate/issues/38>`_ - thank you `MarcoGorelli <https://github.com/MarcoGorelli>`_!).

1.2.0 (2020-05-19)
------------------

Added
^^^^^

* Add ``-n`` / ``--ignore-nested-functions`` flag to ignore nested functions and methods (`#11 <https://github.com/econchick/interrogate/issues/11>`_).
* Add color output for stdout via ``--color``/``--no-color`` (`#25 <https://github.com/econchick/interrogate/issues/25>`_).

Fixed
^^^^^

* Output now alpha-sorts by directory.

1.1.5 (2020-05-12)
------------------

Added
^^^^^

* Add ``__main__.py`` module to allow for invocation via ``python -m interrogate``.

Fixed
^^^^^

* (Windows) Fix commonpath derivation (`#15 <https://github.com/econchick/interrogate/issues/15>`_).
* (Windows) Fix off-by-1 terminal width error (`#20 <https://github.com/econchick/interrogate/issues/20>`_).

Removed
^^^^^^^

* Removed ``networkx`` dependency.

1.1.4 (2020-05-05)
------------------

Added
^^^^^

* Use ``interrogate`` with `pre-commit <https://pre-commit.com/>`_ (addresses `Issue #10 <https://github.com/econchick/interrogate/issues/10>`_).

Fixed
^^^^^

* Fix summary and detail output to fit width of terminal (thank you `psobot <https://github.com/econchick/interrogate/pull/8>`_!).

1.1.3 (2020-05-02)
------------------

Added
^^^^^

* New ``-w/--whitelist-regex`` flag: whitelist regex identifying class, method, and function names to include.

Changed
^^^^^^^

* ``-r/--ignore-regex`` now supports multiple invocations.

Fixed
^^^^^

* Fix misleading bug where module info was still outputted even if ``--ignore-module`` was used.
* Fix output when interrogating a single file where filenames were not listed.

1.1.2 (2020-04-29)
------------------

Fixed
^^^^^

* Fix typo in non-quiet results output (thanks `hynek <https://github.com/econchick/interrogate/pull/5>`_!).

Added
^^^^^

* Add 100% test coverage in the form of functional and unit tests.

1.1.1 (2020-04-27)
------------------

Added
^^^^^

* Improve docstring content to reflect parameters, return values, and raised exceptions.

1.1.0 (2020-04-24)
------------------

Added
^^^^^

* New command to generate a status badge based off of `shields.io <https://shields.io/>`_.

1.0.0.post1 (2020-04-23)
------------------------

Fixed
^^^^^

* Add long description to ``setup.py`` so PyPI is happy.

1.0.0 (2020-04-23)
------------------

Initial release!
