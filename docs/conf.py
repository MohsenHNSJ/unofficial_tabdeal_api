"""Configuration file for the Sphinx documentation builder."""  # noqa: INP001

import re
import sys
from pathlib import Path

# pylint: disable=C0103,W0622

# Path setup
root_path = Path("..")
sys.path.insert(0, (root_path.absolute()).as_uri())

# Version extraction
# Extract version from __init__ file
version = ""

init_file_path = Path("../src/unofficial_tabdeal_api/__init__.py")
with init_file_path.open(encoding="utf-8") as file:
    match: re.Match[str] | None = re.search(
        pattern=r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        string=file.read(),
        flags=re.MULTILINE,
    )
    if match:
        version = match.group(1)
release = version

# Constants
PY_CLASS = "py:class"

# -- Project information -----------------------------------------------------
# Author of project
author = "MohsenHNSJ"
# Copyright license
copyright = "2025, MohsenHNSJ"  # noqa: A001
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns: list[str] = ["_build", "Thumbs.db", ".DS_Store"]
# Language to syntax highlight code blocks
highlight_language = "python3"
# Theme of the documentation
html_theme = "furo"
# Language of documentation text
language = "en"
# The master toctree document
master_doc = "index"
# Minimum required Sphinx
needs_sphinx = "8.2.0"
# Be strict about any broken references
nitpicky = True
# Ignore broken references
nitpick_ignore: set[tuple[str, str]] = {
    (PY_CLASS, "Decimal"),  # Built-in type
    (PY_CLASS, "ClientResponse"),  # aiohttp
    (PY_CLASS, "optional"),  # Documentation
    ("py:exc", "exc_class"),  # Exceptions
}
# Project name
project = "Unofficial Tabdeal API"
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"

# -- General configuration ---------------------------------------------------
# Default extensions
extensions: list[str] = [
    "sphinx.ext.imgconverter",
    "sphinx.ext.duration",
    "versionwarning.extension",
]

# AutoAPI
# Generate complete API documentation without needing to load,
# run, or import the project being documented.
extensions += ["autoapi.extension"]
# Source of the API files [Required]
autoapi_dirs: list[str] = ["../src"]
# Include Type Annotations as Types in Rendered Docstrings
autodoc_typehints = "description"

# Napoleon
# Support for NumPy and Google style docstrings
extensions += ["sphinx.ext.napoleon"]
# True to parse Google style docstrings. False to disable support for Google style docstrings.
napoleon_google_docstring = True
# True to parse NumPy style docstrings. False to disable support for NumPy style docstrings.
napoleon_numpy_docstring = False

# intersphinx
# Link to other projects' documentation
extensions += ["sphinx.ext.intersphinx"]
# This config value contains the locations and names of other projects that
# should be linked to in this documentation.
intersphinx_mapping: dict[str, tuple[str, None]] = {
    "python": ("https://docs.python.org/3/", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

# Add support for nice Not Found 404 pages
extensions += ["notfound.extension"]

# Add a little “copy” button to the right of your code blocks.
extensions += ["sphinx_copybutton"]
