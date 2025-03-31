#!/usr/bin/env bash
# Show Poetry version
poetry about
# Show system information
poetry debug info
# Write the lock file
poetry lock
# Install required packages
poetry install
# Sync and remove unnecessary packages
poetry sync
# Set up the git hook scripts for pre-commit
pre-commit install
