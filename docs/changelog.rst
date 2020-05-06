Changelog
=========

.. short-log

1.1.4 (2020-05-05)
------------------

Added
^^^^^

* Use ``interrogate`` with `pre-commit <https://pre-commit.com/>`_ (addresses `Issue #10 <https://github.com/econchick/interrogate/issues/10>`_).

Fixed
^^^^^

* Fix summary and detail output to fit width of terminal (thank you `psobot <https://github.com/econchick/interrogate/pull/8>`_!).

.. short-log

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
