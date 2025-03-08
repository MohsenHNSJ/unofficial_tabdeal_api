"""This file is a Python file that defines a set of sessions."""
import nox


@nox.session(venv_backend="conda", python=["3.13"])
def ruff_lint(session: nox.sessions.Session) -> None:
    """Lint the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.conda_install("ruff")
    # Show version
    session.run("python", "--version")
    session.run("ruff", "version")
    # Run checks
    session.run("ruff", "check")
