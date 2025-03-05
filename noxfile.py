import nox

# Session for checking and linting the code
@nox.session
def lint(session):
    # Install requirements
    session.install("flake8", "flake8-quotes")
    # Show version of running package
    session.run("flake8", "--version")
    # Run checks
    session.run("flake8", "tests/", "--color", "always")
    session.run("flake8", "src/", "--color", "always")
    session.run("flake8", "docs/", "--color", "always")
    