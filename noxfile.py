"""This file is a Python file that defines a set of sessions."""
import nox


@nox.session
def ruff_lint(session) -> None:
    """Lint the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.install("ruff")
    # Show version
    # session.run("ruff", "")
    # Run checks
    session.run("ruff", "check")