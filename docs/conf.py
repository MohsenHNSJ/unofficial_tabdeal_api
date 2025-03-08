"""Sphinx configuration."""

import os
import re
import sys

sys.path.insert(0, os.path.abspath('..'))

# pylint: disable=C0103,W0622

project = 'Unofficial Tabdeal API'
author = 'MohsenHNSJ'
copyright = '2025, MohsenHNSJ'  # noqa: A001
needs_sphinx = '8.2.0'
highlight_language = 'python3'
language = 'en'

# Extract version from __init__ file
version = ''
with open('../src/unofficial_tabdeal_api/__init__.py', encoding='utf-8') as file:
    match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE
    )
    if match:
        version = match.group(1)

release = version

extensions = [
    'sphinx.ext.imgconverter',
    'sphinx.ext.duration',
    'versionwarning.extension',
]

# HoverXref
extensions += ['hoverxref.extension']
# show a tooltip in all the appearances of the :ref: role
hoverxref_auto_ref = True
hoverxref_intersphinx = [
    'python',
    'aiohttp',
]
hoverxref_domains = [
    'py',
]
# Defining role type to mitigate >>> Using default style (tooltip) for unknown typ (obj).
# Define it in hoverxref_role_types.
hoverxref_role_types = {'obj': 'tooltip'}

# AutoAPI
extensions += ['autoapi.extension']
# Source of the API files
autoapi_dirs = ['../src']
autodoc_typehints = 'description'

# Be strict about any broken references
nitpicky = True

# Napoleon
extensions += ['sphinx.ext.napoleon']
napoleon_google_docstring = True

# intersphinx
extensions += ['sphinx.ext.intersphinx']
# Include Python intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'aiohttp': ('https://docs.aiohttp.org/en/stable/', None),
}

# Add support for nice Not Found 404 pages
extensions += ['notfound.extension']

html_theme = 'furo'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'friendly'
