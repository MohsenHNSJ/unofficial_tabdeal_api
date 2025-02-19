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
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration",
]

nitpicky = True
nitpick_ignore = [
    ("py:class", "aiohttp.client.ClientSession"),  # Bypass referencing to aiohttp
]
# I tried a lot to also reference `aiohttp` but it didn't work
# I tried creating my own `objects.inv` file which had the correct mappings, but it failed with >>>
#       WARNING: failed to reach any of the inventories with the following issues:
#       unknown or unsupported inventory version: ValueError('invalid inventory header: ')
# I tried both manually creating and automatically with `sphobjinv`, but it didn't work.
# The original link also fails with >>>
#       WARNING: py:class reference target not found: aiohttp.client.ClientSession [ref.class]
# I know the problem is with `autodoc` and `intersphinx` but i'm tired of trying to fix it.
# If i could just tell it to map `aiohttp.client.ClientSession` to `aiohttp.ClientSession` somehow...
# It took a lot of time from me, and i'm moving on.
# Also it's not all the fault of `autodoc` and `intersphinx`, `aiohttp.client.ClientSession` actually DOES EXIST in the source code
# but it's not documented and is an implementation detail and it shouldn't be referenced or imported that way.
# # see: https://stackoverflow.com/questions/79448970/cannot-reference-aiohttp-classes-in-my-documentation


napoleon_google_docstring = True

autodoc_typehints = "both"
autodoc_member_order = "alphabetical"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}

html_theme = "furo"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"
