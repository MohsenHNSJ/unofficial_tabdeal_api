#!/bin/bash
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
