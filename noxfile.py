"""This file is a Python file that defines a set of sessions."""
import nox

# Minimum nox required
nox.needs_version = ">=2025.02.09"
# Sessions default backend
nox.options.default_venv_backend = "conda"


@nox.session(venv_backend="conda", python=["3.13"], reuse_venv=True, tags=["lint"])
def ruff_lint(session: nox.sessions.Session) -> None:
    """Lint the code with Ruff.

    Args:
        session (nox.session.Session): An environment and a set of commands to run.
    """
    # Install requirements
    session.run("pip", "install", "--upgrade", "ruff", silent=True)
    # Show version
    session.run("python", "--version")
    session.run("ruff", "version")
    # Run checks
    session.run("ruff", "check")
