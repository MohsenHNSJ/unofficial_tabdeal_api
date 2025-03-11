"""This file is a Python file that defines a set of sessions."""
import shutil
from pathlib import Path

import nox

package_name: str = "unofficial_tabdeal_api"
# Minimum nox required
nox.needs_version = ">=2025.02.09"
# Sessions default backend
nox.options.default_venv_backend = "conda"
# Set an empty list of default sessions to run
# This way, all sessions will not execute on accidental nox calling
nox.options.sessions = []


@nox.session(venv_backend="conda", python=["3.13"], tags=["check"])
def ruff_check(session: nox.sessions.Session) -> None:
    """Check the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run("pip", "install", "--upgrade", "ruff", silent=True)
    # Show version
    session.run("ruff", "version")
    # If argument is provided, append to command to fix errors
    if session.posargs:
        # Join the characters of input argument into a single string
        argument = "".join(session.posargs)
        session.run("ruff", "check", argument)
    else:
        # Else, run checks
        session.run("ruff", "check")


@nox.session(venv_backend="conda", python=["3.13"], tags=["fix"])
def ruff_fix(session: nox.sessions.Session) -> None:
    """Fixes the code with Ruff.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run ruff_check session with autofix
    session.notify("ruff_check", "--fix")


@nox.session(venv_backend="conda", python=["3.13"], tags=["docs"])
def docs_build(session: nox.sessions.Session) -> None:
    """Build the documentation.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Sphinx default arguments
    arguments = ["docs", "docs/_build"]
    # Make output colorful
    arguments.append("--color")
    # Show only warnings and errors
    arguments.append("--quiet")
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", "--upgrade", "-r",
                "docs/requirements.txt", silent=True)
    # Set build path
    build_dir = Path("docs", "_build")
    # If build path exists, clear it
    if build_dir.exists():
        shutil.rmtree(build_dir)
    # If argument is provided, run autobuild
    if session.posargs:
        # Join the characters of input argument into a single string
        argument = "".join(session.posargs)
        # Add the argument to beginning of the list
        arguments.insert(0, argument)
        # Run documentation build and live preview
        session.run("sphinx-autobuild", *arguments)
    else:
        # Run documentation build only
        session.run("sphinx-build", *arguments)


@nox.session(venv_backend="conda", python=["3.13"], tags=["preview"])
def docs_preview(session: nox.sessions.Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run documentation build with live preview
    session.notify("docs_build", "--open-browser")


@nox.session(venv_backend="conda", python=["3.13"], tags=["type"])
def mypy_check(session: nox.sessions.Session) -> None:
    """Type check using MyPy.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # MyPy default check locations
    arguments = ["src", "tests", "docs/conf.py"]
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", "--upgrade", "mypy", "pytest", silent=True)
    # Show version
    session.run("mypy", "--version")
    # Run MyPy type checking
    session.run("mypy", *arguments)
