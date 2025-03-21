"""This file is a Python file that defines a set of sessions."""
import shutil
from pathlib import Path

import nox
import nox.sessions

package_name: str = "unofficial_tabdeal_api"
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
    session.run("pip", "install", "--upgrade", "ruff", silent=True)
    # Show version
    session.run("ruff", "version")
    # Show tested version
    print("=========="
          f"{green_text}Tested with Ruff 0.11.0\n"
          f"{white_text}If the installed version is above the tested version\n"
          "Consider reading the changelog and implement necessary changes\n"
          f"{cyan_text}https://github.com/astral-sh/ruff/releases\n"
          f"{white_text}==========")
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
    session.run("pip", "install", "--upgrade", "-r",
                "docs/requirements.txt", silent=True)
    # Show version
    session.run("sphinx-build", "--version")
    # Show tested version
    print("=========="
          f"{green_text}Tested with Sphinx 8.2.3\n"
          f"{white_text}If the installed version is above the tested version\n"
          "Consider reading the changelog and implement necessary changes\n"
          f"{cyan_text}https://www.sphinx-doc.org/en/master/changes/"
          f"{white_text}==========")
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
    session.run("pip", "install", "--upgrade", "mypy", "pytest", silent=True)
    # Show version
    session.run("mypy", "--version")
    # Show tested version
    print("=========="
          f"{green_text}Tested with MyPy 1.15.0\n"
          f"{white_text}If the installed version is above the tested version\n"
          "Consider reading the changelog and implement necessary changes\n"
          f"{cyan_text}https://mypy.readthedocs.io/en/stable/changelog.html"
          f"{white_text}==========")
    # Run MyPy type checking
    session.run("mypy", *arguments)


# @nox.session(python=["3.10", "3.13"], tags=["test"])
@nox.session(python=["3.13"], tags=["test"])
def pytest_test(session: nox.sessions.Session) -> None:
    """Run the test suit.

    Args:
        session (nox.sessions.Session): An environment and a set of commands to run.
    """
    # Install the package
    session.install(".")
    # Install requirements
    session.run("pip", "install", "--upgrade",
                "pytest", silent=True)
    # asyncio plugin
    session.run("pip", "install", "--upgrade",
                "pytest-asyncio", silent=True)
    # aiohttp plugin
    session.run("pip", "install", "--upgrade",
                "pytest-aiohttp", silent=True)
    # Show version
    session.run("pytest", "--version")
    # Show tested version
    print("==========\n"
          f"{green_text}Tested with Pytest 8.3.5\n"
          f"{white_text}If the installed version is above the tested version\n"
          "Consider reading the changelog and implement necessary changes\n"
          f"{cyan_text}https://docs.pytest.org/en/stable/changelog.html\n"
          f"{white_text}==========")
    print("Plugin versions tested:\n"
          f"{green_text}pytest-asyncio tested at 0.25.3\n"
          f"{cyan_text}https://github.com/pytest-dev/pytest-asyncio\n"
          f"{green_text}pytest-aiohttp tested at 1.1.0\n"
          f"{cyan_text}https://github.com/aio-libs/pytest-aiohttp\n"
          f"{white_text}==========")
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
    session.run("pip", "install", "--upgrade",
                "pytest", silent=True)
    # codspeed plugin
    session.run("pip", "install", "--upgrade",
                "pytest-codspeed", silent=True)
    # asyncio plugin
    session.run("pip", "install", "--upgrade",
                "pytest-asyncio", silent=True)
    # Show version
    session.run("pytest", "--version")
    # Show tested version
    print("==========\n"
          f"{green_text}Tested with Pytest 8.3.5\n"
          f"{white_text}If the installed version is above the tested version\n"
          "Consider reading the changelog and implement necessary changes\n"
          f"{cyan_text}https://docs.pytest.org/en/stable/changelog.html\n"
          f"{white_text}==========")
    print("Plugin versions tested:\n"
          f"{green_text}pytest-codspeed tested at 3.2.0\n"
          f"{cyan_text}https://github.com/CodSpeedHQ/pytest-codspeed\n"
          f"{green_text}pytest-asyncio tested at 0.25.3\n"
          f"{cyan_text}https://github.com/pytest-dev/pytest-asyncio\n"
          f"{white_text}==========")
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
    session.run("pip", "install", "--upgrade", "coverage",
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
