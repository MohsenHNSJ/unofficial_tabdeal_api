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
    'sphinx.ext.autosummary',
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration",
    "sphinx.ext.viewcode",
]

nitpicky = True
nitpick_ignore = [
    ("py:mod", "aiohttp"),  # undocumented, no `.. currentmodule:: aiohttp` in docs
    ("py:class", "aiohttp.client.ClientSession"),  # TEMPORARY ERROR BYPASS - NEED TO FIX IT
    ("py:class", "aiohttp.SimpleCookie"),  # undocumented
    ("py:class", "aiohttp.web.RequestHandler"),  # undocumented
    ("py:class", "aiohttp.NamedPipeConnector"),  # undocumented
    ("py:class", "aiohttp.protocol.HttpVersion"),  # undocumented
    ("py:class", "aiohttp.ClientRequest"),  # undocumented
    ("py:class", "aiohttp.payload.Payload"),  # undocumented
    ("py:class", "aiohttp.resolver.AsyncResolver"),  # undocumented
    ("py:class", "aiohttp.resolver.ThreadedResolver"),  # undocumented
    ("py:func", "aiohttp.ws_connect"),  # undocumented
    ("py:meth", "start"),  # undocumented
    ("py:exc", "aiohttp.ClientHttpProxyError"),  # undocumented
    ("py:class", "asyncio.AbstractServer"),  # undocumented
    ("py:mod", "aiohttp.test_tools"),  # undocumented
    ("py:class", "list of pairs"),  # undocumented
    ("py:class", "aiohttp.protocol.HttpVersion"),  # undocumented
    ("py:meth", "aiohttp.ClientSession.request"),  # undocumented
    ("py:class", "aiohttp.StreamWriter"),  # undocumented
    ("py:attr", "aiohttp.StreamResponse.body"),  # undocumented
    ("py:class", "aiohttp.payload.StringPayload"),  # undocumented
    ("py:meth", "aiohttp.web.Application.copy"),  # undocumented
    ("py:meth", "asyncio.AbstractEventLoop.create_server"),  # undocumented
    ("py:data", "aiohttp.log.server_logger"),  # undocumented
    ("py:data", "aiohttp.log.access_logger"),  # undocumented
    ("py:data", "aiohttp.helpers.AccessLogger"),  # undocumented
    ("py:attr", "helpers.AccessLogger.LOG_FORMAT"),  # undocumented
    ("py:meth", "aiohttp.web.AbstractRoute.url"),  # undocumented
    ("py:class", "aiohttp.web.MatchedSubAppResource"),  # undocumented
    ("py:attr", "body"),  # undocumented
    ("py:class", "socket.socket"),  # undocumented
    ("py:class", "socket.AddressFamily"),  # undocumented
    ("py:obj", "logging.DEBUG"),  # undocumented
    ("py:class", "aiohttp.abc.AbstractAsyncAccessLogger"),  # undocumented
    ("py:meth", "aiohttp.web.Response.write_eof"),  # undocumented
    ("py:meth", "aiohttp.payload.Payload.set_content_disposition"),  # undocumented
    ("py:class", "cgi.FieldStorage"),  # undocumented
    ("py:meth", "aiohttp.web.UrlDispatcher.register_resource"),  # undocumented
    ("py:func", "aiohttp_debugtoolbar.setup"),  # undocumented
]

napoleon_google_docstring = True

autodoc_typehints = "description"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'aiohttp': ('https://docs.aiohttp.org/en/stable/', None),
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
