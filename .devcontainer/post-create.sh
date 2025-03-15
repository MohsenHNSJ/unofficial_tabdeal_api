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
# poetry sync
# Install other python versions for testing
poetry python install 3.10
poetry python install 3.11
poetry python install 3.12
