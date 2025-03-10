"""This file is a Python file that defines a set of sessions."""
import shutil
from pathlib import Path

import nox

# Documentation build requirements
doc_build_requirements = ["sphinx", "sphinx-autobuild", "furo", "sphinx-autoapi",
                          "sphinx-hoverxref", "sphinx-notfound-page", "sphinx-version-warning"]
# Minimum nox required
nox.needs_version = ">=2025.02.09"
# Sessions default backend
nox.options.default_venv_backend = "conda"
# Set an empty list of default sessions to run
# This way, all sessions will not execute on accidental nox calling
nox.options.sessions = []


@nox.session(venv_backend="conda", python=["3.13"], reuse_venv=True, tags=["check"])
def ruff_check(session: nox.sessions.Session) -> None:
    """Check the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run("pip", "install", "--upgrade", "ruff", silent=True)
    # Show version
    session.run("python", "--version")
    session.run("ruff", "version")
    # If argument is provided, append to command
    if session.posargs:
        # Join the characters of input argument into a single string
        argument = "".join(session.posargs)
        session.run("ruff", "check", argument)
    else:
        # Else, run checks
        session.run("ruff", "check")


@nox.session(venv_backend="conda", python=["3.13"], reuse_venv=True, tags=["fix"])
def ruff_fix(session: nox.sessions.Session) -> None:
    """Fixes the code with Ruff.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    session.notify("ruff_check", "--fix")


@nox.session(venv_backend="conda", python=["3.13"], reuse_venv=True, tags=["preview"])
def preview_docs(session: nox.sessions.Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    args = ["--open-browser", "docs", "docs/_build"]
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", "--upgrade",
                *doc_build_requirements, silent=True)
    # Set build path
    build_dir = Path("docs", "_build")
    # If build path exists, clear it
    if build_dir.exists():
        shutil.rmtree(build_dir)
    # Run documentation building
    session.run("sphinx-autobuild", *args)
