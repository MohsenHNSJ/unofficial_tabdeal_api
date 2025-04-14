"""Sphinx configuration."""

import re
import sys
from pathlib import Path

# sys.path.insert(0, os.path.abspath(".."))
root_path = Path("..")
sys.path.insert(0, (root_path.absolute()).as_uri())

# pylint: disable=C0103,W0622

# Author of project
author = "MohsenHNSJ"
# Copyright license
copyright = "2025, MohsenHNSJ"  # noqa: A001
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
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
# Project name
project = "Unofficial Tabdeal API"
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"

# Extract version from __init__ file
version = ""
# with open("../src/unofficial_tabdeal_api/__init__.py", encoding="utf-8") as file:
#     match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE)
#     if match:
#         version = match.group(1)

init_file_path = Path("../src/unofficial_tabdeal_api/__init__.py")
with init_file_path.open(encoding="utf-8") as file:
    match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        file.read(),
        re.MULTILINE,
    )
    if match:
        version = match.group(1)
release = version

# Default extensions
extensions = [
    "sphinx.ext.imgconverter",
    "sphinx.ext.duration",
    "versionwarning.extension",
]

# HoverXref
# Show a floating window (tooltips or modal dialogues) on the cross references of the documentation
# embedding the content of the linked section on them.
extensions += ["hoverxref.extension"]
# Show a tooltip in all the appearances of the :ref: role
hoverxref_auto_ref = True
# Enable Sphinx's hoverxref extension on intersphinx targets from intersphinx_mapping.
hoverxref_intersphinx = [
    "python",
    "aiohttp",
]
# List containing the Sphinx Domain's names where hoverxref has to be applied.
hoverxref_domains = [
    "py",
]
# Defining role type to mitigate >>> Using default style (tooltip) for unknown typ (obj).
# Define it in hoverxref_role_types.
hoverxref_role_types = {"obj": "tooltip"}

# AutoAPI
# Generate complete API documentation without needing to load,
# run, or import the project being documented.
extensions += ["autoapi.extension"]
# Source of the API files [Required]
autoapi_dirs = ["../src"]
# Include Type Annotations as Types in Rendered Docstrings
autodoc_typehints = "description"

# Napoleon
# Support for NumPy and Google style docstrings
extensions += ["sphinx.ext.napoleon"]
# rue to parse Google style docstrings. False to disable support for Google style docstrings.
napoleon_google_docstring = True

# intersphinx
# Link to other projects' documentation
extensions += ["sphinx.ext.intersphinx"]
# This config value contains the locations and names of other projects that
# should be linked to in this documentation.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}

# Add support for nice Not Found 404 pages
extensions += ["notfound.extension"]

# Add a little “copy” button to the right of your code blocks.
extensions += ["sphinx_copybutton"]
