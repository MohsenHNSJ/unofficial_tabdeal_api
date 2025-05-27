# https://github.com/devcontainers/images/tree/main/src/python
FROM mcr.microsoft.com/devcontainers/python:3

# Create a usergroup and user for VS Code
RUN groupadd -r vscode && useradd --no-log-init -r -g vscode vscode

# Switch to the vscode user
USER vscode
