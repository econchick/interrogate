# How To Contribute

First off, thank you for considering contributing to `interrogate`! It's people like _you_ who make it such a great tool for everyone.

This document intends to make contribution more accessible by codifying tribal knowledge and expectations. Don't be afraid to open half-finished PRs, and ask questions if something is unclear!

## Workflow

* No contribution is too small! Please submit as many fixes for typos and grammar bloopers as you can!
* Try to limit each pull request to _one_ change only.
* Since we squash on merge, it's up to you how you handle updates to the master branch. Whether you prefer to rebase on master or merge master into your branch, do whatever is more comfortable for you.
* _Always_ add tests and docs for your code. This is a hard rule; patches with missing tests or documentation will not be merged.
* Make sure your changes pass our [CI](https://github.com/econchick/interrogate/actions?query=workflow%3ACI). You won't get any feedback until it's green unless you ask for it.
* Once you've addressed review feedback, make sure to bump the pull request with a short note, so we know you're done.
* Avoid breaking backwards compatibility.

## Code

* Obey [PEP 8](https://www.python.org/dev/peps/pep-0008/), [PEP 257](https://www.python.org/dev/peps/pep-0257/), and the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html) (mostly[^mostly]).  We use [restructuredtext](https://docutils.sourceforge.io/rst.html) syntax, and have a summary line starting the `"""` block:

    ```python
    def func(x):
        """Do something.

        Maybe some more "something" context that can span
        multiple lines.

        :param str x: A very important parameter.
        :rtype: str
        """
    ```
* If you add or change public APIs, tag the docstring using [version directives](http://www.sphinx-doc.org/en/stable/markup/para.html#directive-versionadded) like `..  versionadded:: 1.2.0 WHAT` or `..  versionchanged:: 1.2.1 WHAT`.
* We follow the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html) for sorting our imports enforced by [isort](https://github.com/timothycrosley/isort), and we follow the [Black](https://github.com/psf/black) code style with a line length of 79 characters.As long as you run our full tox suite before committing, or install our [pre-commit](https://pre-commit.com/) hooks (ideally you'll do both -- see [Local Development Environment](#local-development-environment)), you won't have to spend any time on formatting your code at all. If you don't, CI will catch it for you -- but that seems like a waste of your time!

[^mostly]: Due to personal preference, this project differs from Google's style guide in a few ways:
    * Instead of using Google's approach for documenting [arguments, return/yields, and raises](http://google.github.io/styleguide/pyguide.html#383-functions-and-methods), use [restructuredtext](https://docutils.sourceforge.io/rst.html) syntax as recommended by [PEP-0258](https://www.python.org/dev/peps/pep-0258/).
    * Instead of [using `pylint`](http://google.github.io/styleguide/pyguide.html#21-lint), use [flake8](https://flake8.pycqa.org/en/latest/).
    * Instead of [using yapf](http://google.github.io/styleguide/pyguide.html#1-background), use [Black](https://github.com/psf/black).


## Tests

* Write your asserts as `expected == actual` to line them up nicely:

    ```python

     x = f()

     assert 42 == x.some_attribute
     assert "foo" == x._a_private_attribute
    ```

* To run the test suite, all you need is a recent [tox](https://tox.readthedocs.io/). It will ensure the test suite runs with all dependencies against all Python versions just as it will in our CI. If you lack some Python versions, you can can always limit the environments like ``tox -e py36,py37`` (in that case you may want to look into [pyenv](https://github.com/pyenv/pyenv), which makes it very easy to install many different Python versions in parallel).
* Write [good test docstrings](https://jml.io/pages/test-docstrings.html).

## Documentation

Project-related documentation is written in [restructuredtext](https://docutils.sourceforge.io/rst.html) (`.rst`). GitHub-related project documentation (e.g. this file you're reading, `CONTRIBUTING.md`) is written in Markdown, as GitHub doesn't support `.rst` files for some of their features (e.g. automatically picking up the `CODE_OF_CONDUCT.md`)

* If you start a new section, add two blank lines before and one blank line after the header, except if two headers follow immediately after each other:

    ```rst
     Last line of previous section.

     Header of New Top Section
     -------------------------

     Header of New Section
     ^^^^^^^^^^^^^^^^^^^^^

     First line of new section.
     ```

* If you add a new feature, demonstrate its awesomeness under `Usage` in `README.rst`!

## Local Development Environment

You can (and should) run our test suite using [tox](https://tox.readthedocs.io/). However, you’ll probably want a more traditional environment as well. We highly recommend to develop using the latest Python 3 release because `interrogate` tries to take advantage of modern features whenever possible.

First create a [virtual environment](https://virtualenv.pypa.io/). It’s out of scope for this document to list all the ways to manage virtual environments in Python, but if you don’t already have a pet way, take some time to look at tools like [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv), [pew](https://github.com/berdario/pew), [virtualfish](https://virtualfish.readthedocs.io/), [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/), and [pyenv-virtualenvwrapper](https://github.com/pyenv/pyenv-virtualenvwrapper).

Next, get an up to date checkout of the `interrogate` repository:

```console
$ git clone git@github.com:econchick/interrogate.git
```

or if you want to use git via `https`:

```console
$ git clone https://github.com/econchick/interrogate.git
```

Change into the newly created directory and **after activating your virtual environment** install an editable version of `interrogate` along with its tests and docs requirements:

```console
(env) $ cd interrogate
(env) $ pip install -e '.[dev]'
```

At this point,

```console
(env) $ python -m pytest
```

should work and pass, as should:

```console
(env) $ cd docs
(env) $ make livehtml
```

The built documentation can then be found in [`localhost:8888`](http://localhost:8888).

To avoid committing code that violates our style guide, we advise you to install [pre-commit](https://pre-commit.com/)[^pre] hooks:

```console
(env) $ pre-commit install
```

You can also run them anytime (as our `tox` does, but always run `tox` outside of a virtual environment):

```console
(env) $ pre-commit run --all-files
```

[^pre]: pre-commit should have been installed into your virtualenv automatically when you ran `pip install -e '.[dev]'` above. If pre-commit is missing, it may be that you need to re-run `pip install -e '.[dev]'`.


## Code of Conduct

Please note that this project is released with a Contributor [Code of Conduct](https://github.com/econchick/interrogate/blob/master/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms. Please report any harm to `interrogate-project [at] lynnroot.com` for anything you find appropriate.

Thank you for considering contributing to `interrogate`!
