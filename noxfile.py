"""This file is a Python file that defines a set of sessions."""

import shutil
from pathlib import Path

import nox
import nox.sessions

# Package name
package_name: str = "unofficial_tabdeal_api"
# Python version for environments
python_version: list[str] = ["3.13"]

# region NOX
# Minimum nox required
nox.needs_version = "==2025.02.09"
# Sessions default backend
nox.options.default_venv_backend = "venv"
# Set an empty list of default sessions to run
# This way, all sessions will not execute on accidental nox calling
nox.options.sessions = []
# endregion NOX

# region PIP
# Constraint command for pip
constraint: str = "--constraint=.github/workflows/constraints.txt"
# Pip install command
pip_install: list[str] = ["pip", "install"]
# endregion PIP

# region SPHINX
# Sphinx build command | Colorful output | Show only warnings and errors
sphinx_build: list[str] = ["docs", "docs/_build", "--color", "--quiet"]
# Documentation requirements
docs_requirements: list[str] = ["-r", "docs/requirements.txt"]
# Documentation build path
docs_build_path = Path("docs", "_build")
# endregion SPHINX

# region MYPY
# MyPy default check locations
mypy_commands: list[str] = ["src", "tests", "docs/conf.py"]
# MyPy requirements
mypy_requirements: list[str] = ["mypy", "pytest"]
# endregion MYPY

# region PYTEST
# Pytest requirements
pytest_requirements: list[str] = [
    "pytest",
    "coverage",
    "pytest-asyncio",
    "pytest-aiohttp",
    "pytest-codspeed",
]
# Benchmark commands
benchmark_commands: list[str] = ["pytest", "tests/", "--codspeed", "-rA"]
# endregion PYTEST

# region PRE-COMMIT
pre_commit_commands: list[str] = [
    "pre-commit",
    "run",
    "--all-files",
    "--show-diff-on-failure",
]
# endregion PRE-COMMIT


@nox.session(python=python_version, tags=["check"])
def ruff_check(session: nox.sessions.Session) -> None:
    """Check the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run(*pip_install, constraint, "ruff", silent=True)
    # If argument is provided, append to command to fix errors
    if session.posargs:
        # Join the characters of input argument into a single string
        argument: str = "".join(session.posargs)
        session.run("ruff", "check", argument)
    else:
        # Else, run checks
        session.run("ruff", "check")


@nox.session(python=python_version, tags=["fix"])
def ruff_fix(session: nox.sessions.Session) -> None:
    """Fixes the code with Ruff.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run ruff_check session with autofix
    session.notify("ruff_check", "--fix")


@nox.session(python=python_version, tags=["docs"])
def docs_build(session: nox.sessions.Session) -> None:
    """Build the documentation.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".", silent=True)
    # Install requirements
    session.run(*pip_install, *docs_requirements, silent=True)
    # If build path exists, clear it
    if docs_build_path.exists():
        shutil.rmtree(docs_build_path)
    # If argument is provided, run autobuild
    if session.posargs:
        # Join the characters of input argument into a single string
        argument: str = "".join(session.posargs)
        # Add the argument to beginning of the list
        sphinx_build.insert(0, argument)
        # Run documentation build and live preview
        session.run("sphinx-autobuild", *sphinx_build)
    else:
        # Run documentation build only
        session.run("sphinx-build", *sphinx_build)


@nox.session(python=python_version, tags=["preview"])
def docs_preview(session: nox.sessions.Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run documentation build with live preview
    session.notify("docs_build", "--open-browser")


@nox.session(python=python_version, tags=["type"])
def mypy_check(session: nox.sessions.Session) -> None:
    """Type check using MyPy.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".", silent=True)
    # Install requirements
    session.run(*pip_install, constraint, *mypy_requirements, silent=True)
    # Run MyPy type checking
    session.run("mypy", *mypy_commands)


@nox.session(python=["3.11", "3.13"], tags=["test"])
def test(session: nox.sessions.Session) -> None:
    """Runs the test suite and generates coverage data.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".", silent=True)
    # Install requirements
    session.run(*pip_install, constraint, *pytest_requirements, silent=True)
    # Run tests
    session.run("coverage", "run", "--parallel", "-m", "pytest", "-rA")


@nox.session(python=python_version, tags=["coverage"])
def coverage(session: nox.sessions.Session) -> None:
    """Produce coverage report.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run(*pip_install, constraint, "coverage", silent=True)
    # Combine coverage data
    session.run("coverage", "combine")
    # Report the combined data
    session.run("coverage", "report")


@nox.session(python=python_version, tags=["test_and_coverage"], requires=["test"])
def test_and_coverage(session: nox.sessions.Session) -> None:
    """Run the test suit and produce coverage report.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run the coverage session, after testing session
    session.notify("coverage")


@nox.session(python=python_version, tags=["benchmark"])
def benchmark(session: nox.sessions.Session) -> None:
    """Runs the benchmarks.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".", silent=True)
    # Install requirements
    session.run(*pip_install, constraint, *pytest_requirements, silent=True)
    # Run pytest for codspeed
    session.run(*benchmark_commands)


@nox.session(name="pre-commit", python=python_version, tags=["pre-commit"])
def pre_commit(session: nox.sessions.Session) -> None:
    """Runs pre-commit hooks.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run(*pip_install, constraint, "pre-commit", silent=True)
    # Run pre-commit
    session.run(*pre_commit_commands)
