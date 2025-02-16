"""Sphinx configuration."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', 'src').resolve()))

# pylint: disable=C0103,W0622

project = "Unofficial Tabdeal Api"
author = "MohsenHNSJ"
copyright = "2025, MohsenHNSJ"
version = release = "0.1.2"
needs_sphinx = "8.1.3"
highlight_language = "python3"
nitpicky = True
language = "en"
extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    'sphinx.ext.autosummary',
    "sphinx.ext.imgconverter",
]
autodoc_typehints = "description"
html_theme = "furo"
