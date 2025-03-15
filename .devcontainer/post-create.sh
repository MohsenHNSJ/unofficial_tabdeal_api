#!/usr/bin/env bash
# Show Poetry version
poetry about
# Show system information
poetry debug info
# Write the lock file
poetry lock
# Sync and remove unnecessary packages
poetry sync
# Check lock file strictly
poetry check --strict