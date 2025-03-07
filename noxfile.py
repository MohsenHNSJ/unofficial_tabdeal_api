"""This file is a Python file that defines a set of sessions."""
import nox


# Session for checking and linting the code
@nox.session
def lint(session: nox.session.Session) -> None:
    """Lints the code with Flake8 and Ruff

    Args:
        session (nox.session.Session): An environment and a set of commands to run in that environment.
    """
    # Install requirements
    session.install("flake8", "flake8-quotes")
    # Show version of running package
    session.run("flake8", "--version")
    # Run checks
    session.run("flake8", "tests/", "--color", "always")
    session.run("flake8", "src/", "--color", "always")
    session.run("flake8", "docs/", "--color", "always")
