"""Sphinx configuration."""

import sys
import os

sys.path.insert(0, os.path.abspath(".."))

# pylint: disable=C0103,W0622

project = "Unofficial Tabdeal API"
author = "MohsenHNSJ"
copyright = "2025, MohsenHNSJ"
version = release = "0.1.2"
needs_sphinx = "8.1.3"
highlight_language = "python3"
language = "en"

extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    'sphinx.ext.autosummary',
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration",
]

nitpicky = True

napoleon_google_docstring = True

autodoc_typehints = "description"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None)
}

# Change the default role so we can avoid prefixing everything with :obj:
default_role = "py:obj"

html_theme = "furo"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"
