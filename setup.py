#! /usr/bin/env python
# Copyright 2020 Lynn Root

import codecs
import os
import re

from setuptools import find_packages, setup


HERE = os.path.abspath(os.path.dirname(__file__))


#####
# Helper functions
#####
def read(*filenames, **kwargs):
    """
    Build an absolute path from ``*filenames``, and  return contents of
    resulting file.  Defaults to UTF-8 encoding.
    """
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for fl in filenames:
        with codecs.open(os.path.join(HERE, fl), "rb", encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def find_meta(meta):
    """Extract __*meta*__ from META_FILE."""
    re_str = rf"^__{meta}__ = ['\"]([^'\"]*)['\"]"
    meta_match = re.search(re_str, META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.")


#####
# Project-specific constants
#####
NAME = "interrogate"
PACKAGE_NAME = "interrogate"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", PACKAGE_NAME, "__init__.py")

META_FILE = read(META_PATH)
KEYWORDS = ["documentation", "coverage", "quality"]
PROJECT_URLS = {
    "Documentation": "https://interrogate.readthedocs.io",
    "Bug Tracker": "https://github.com/econchick/interrogate/issues",
    "Source Code": "https://github.com/econchick/interrogate",
}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
]
INSTALL_REQUIRES = [
    "attrs",
    "click>=7.1",
    "colorama",
    "py",
    "tabulate",
    "tomli; python_version < '3.11'",
]
EXTRAS_REQUIRE = {
    "png": ["cairosvg"],
    "docs": ["sphinx", "sphinx-autobuild"],
    "tests": ["pytest", "pytest-cov", "pytest-mock", "coverage[toml]"],
    "typing": ["mypy", "types-tabulate"],
}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["png"]
    + EXTRAS_REQUIRE["docs"]
    + EXTRAS_REQUIRE["tests"]
    + EXTRAS_REQUIRE["typing"]
    + ["wheel", "pre-commit"]
)
URL = find_meta("uri")
LONG = (
    read("README.rst")
    + "\n"
    + "Release Information\n"
    + "==================="
    + read("docs/changelog.rst").split(".. short-log")[1]
    + "\n`Full changelog "
    + f"<{URL}/en/latest/#changelog>`_."
)

setup(
    name=NAME,
    version=find_meta("version"),
    description=find_meta("description"),
    long_description=LONG,
    long_description_content_type="text/x-rst",
    url=URL,
    project_urls=PROJECT_URLS,
    author=find_meta("author"),
    author_email=find_meta("email"),
    maintainer=find_meta("author"),
    maintainer_email=find_meta("email"),
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": ["interrogate = interrogate.cli:main"],
    },
    classifiers=CLASSIFIERS,
)
