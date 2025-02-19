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
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration",
    "autoapi.extension",
    'hoverxref.extension',
]

autoapi_dirs = ['../src']
autodoc_typehints = "description"

# show a tooltip in all the appearances of the :ref: role
hoverxref_auto_ref = True

nitpicky = True

napoleon_google_docstring = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}

hoverxref_intersphinx = [
    "python",
    "aiohttp",
]

hoverxref_domains = [
    "py",
]

html_theme = "furo"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"
