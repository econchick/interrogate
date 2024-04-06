import codecs
import os
import re


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), "rb", "utf-8") as f:
        return f.read()


def find_version(*file_paths):
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# -- Project information -----------------------------------------------------

project = "interrogate"
copyright = "2020, Lynn Root"
author = "Lynn Root"

# The short X.Y version.
release = find_version("../src/interrogate/__init__.py")
version = release.rsplit(".", 1)[0]

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme_options = {
    "font_size": "18px",
    # "page_width": "1020px",
    "github_button": False,
    "github_user": "econchick",
    "github_repo": "interrogate",
    "link": "#de78a0",
    "link_hover": "#de78a0",
    "description": "interrogate: measure docstring coverage",
    "fixed_sidebar": True,
    "sidebar_collapse": False,
    "logo": "logo_pink.png",
    "font_family": '"Avenir Next", Calibri, "PT Sans", sans-serif',
    "head_font_family": '"Avenir Next", Calibri, "PT Sans", sans-serif',
    # "show_relbars": True,
    # "sidebar_includehidden": True,
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_favicon = "_static/favicon.png"
html_css_files = [
    "custom.css",
]
templates_path = ["_templates"]
html_title = f"Python docstring coverage (v{release})"
html_short_title = "interrogate: Python docstring coverage"

# -- Other config

# For when I want to turn on API documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "click": ("https://click.palletsprojects.com/en/7.x/", None),
}
autodoc_member_order = "bysource"
