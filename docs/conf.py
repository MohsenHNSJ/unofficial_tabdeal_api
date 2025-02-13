"""Sphinx configuration."""

# pylint: disable=C0103,W0622

project = "Unofficial Tabdeal Api"
author = "MohsenHNSJ"
copyright = "2025, MohsenHNSJ"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
