"""This file is a Python file that defines a set of sessions."""
import shutil
from pathlib import Path

import nox
import nox.sessions

package_name: str = "unofficial_tabdeal_api"
constraint: str = "--constraint=.github/workflows/constraints.txt"
# Minimum nox required
nox.needs_version = "==2025.02.09"
# Sessions default backend
nox.options.default_venv_backend = "venv"
# Set an empty list of default sessions to run
# This way, all sessions will not execute on accidental nox calling
nox.options.sessions = []

# Colors for printing text
green_text: str = "\033[38;5;2m"
white_text: str = "\033[38;5;255m"
cyan_text: str = "\033[38;5;75m"


@nox.session(python=["3.13"], tags=["check"])
def ruff_check(session: nox.sessions.Session) -> None:
    """Check the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run("pip", "install", constraint, "ruff", silent=True)
    # If argument is provided, append to command to fix errors
    if session.posargs:
        # Join the characters of input argument into a single string
        argument: str = "".join(session.posargs)
        session.run("ruff", "check", argument)
    else:
        # Else, run checks
        session.run("ruff", "check")


@nox.session(python=["3.13"], tags=["fix"])
def ruff_fix(session: nox.sessions.Session) -> None:
    """Fixes the code with Ruff.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run ruff_check session with autofix
    session.notify("ruff_check", "--fix")


@nox.session(python=["3.13"], tags=["docs"])
def docs_build(session: nox.sessions.Session) -> None:
    """Build the documentation.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Sphinx default arguments
    arguments: list[str] = ["docs", "docs/_build"]
    # Make output colorful
    arguments.append("--color")
    # Show only warnings and errors
    arguments.append("--quiet")
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", "-r",
                "docs/requirements.txt", silent=True)
    # Set build path
    build_dir = Path("docs", "_build")
    # If build path exists, clear it
    if build_dir.exists():
        shutil.rmtree(build_dir)
    # If argument is provided, run autobuild
    if session.posargs:
        # Join the characters of input argument into a single string
        argument: str = "".join(session.posargs)
        # Add the argument to beginning of the list
        arguments.insert(0, argument)
        # Run documentation build and live preview
        session.run("sphinx-autobuild", *arguments)
    else:
        # Run documentation build only
        session.run("sphinx-build", *arguments)


@nox.session(python=["3.13"], tags=["preview"])
def docs_preview(session: nox.sessions.Session) -> None:
    """Build and serve the documentation with live reloading on file changes.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run documentation build with live preview
    session.notify("docs_build", "--open-browser")


@nox.session(python=["3.13"], tags=["type"])
def mypy_check(session: nox.sessions.Session) -> None:
    """Type check using MyPy.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # MyPy default check locations
    arguments: list[str] = ["src", "tests", "docs/conf.py"]
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", constraint, "mypy", "pytest", silent=True)
    # Run MyPy type checking
    session.run("mypy", *arguments)


# @nox.session(python=["3.11", "3.13"], tags=["test"])
@nox.session(python=["3.13"], tags=["test"])
def pytest_test(session: nox.sessions.Session) -> None:
    """Run the test suit.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", constraint,
                "pytest", silent=True)
    # asyncio plugin
    session.run("pip", "install", constraint,
                "pytest-asyncio", silent=True)
    # aiohttp plugin
    session.run("pip", "install", constraint,
                "pytest-aiohttp", silent=True)
    # Run pytest
    session.run("pytest", "-rA")


@nox.session(python=["3.13"], tags=["benchmark"])
def pytest_benchmark(session: nox.sessions.Session) -> None:
    """Runs the benchmarks.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", constraint,
                "pytest", silent=True)
    # codspeed plugin
    session.run("pip", "install", constraint,
                "pytest-codspeed", silent=True)
    # asyncio plugin
    session.run("pip", "install", constraint,
                "pytest-asyncio", silent=True)
    # Run pytest for codspeed
    session.run("pytest", "tests/", "--codspeed", "-rA")


# TODO: INCOMPLETE
@nox.session(python=["3.13"], tags=["coverage"])
def coverage_report(session: nox.sessions.Session) -> None:
    """Produce the coverage report.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # TODO: Add show tested version
    # TODO: Complete the coverage testing and reporting
    # Default Coverage arguments
    arguments: list[str] = ["run", "--parallel", "-m", "pytest", package_name]
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", constraint, "coverage",
                "pytest", "pygments", silent=True)
    # Run coverage
    session.run("coverage", *arguments)


@nox.session(python=["3.13"], tags=["all"])
def run_all_tests(session: nox.sessions.Session) -> None:
    """Runs all the required tests before committing.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Run ruff lint
    session.notify("ruff_check")
    # Run documentation building
    session.notify("docs_build")
    # Run mypy type checker
    session.notify("mypy_check")
    # Run pytest tests
    session.notify("pytest_test")
