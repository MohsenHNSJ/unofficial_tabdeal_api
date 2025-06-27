#!/bin/bash
# This script is executed after the container is created.
# It sets up the development environment by installing dependencies and configuring the project.
# Ensure the script exits on any error
set -e

# Show Poetry version
echo "Poetry version:"
# This will show the Poetry version installed in the container
poetry about

# Show system information
echo "System information:"
# This will show the Python version, Poetry version, and other relevant information
poetry debug info

# Write the lock file
echo "Writing Poetry lock file..."
# This will resolve dependencies and create a poetry.lock file
poetry lock

# Install required packages
echo "Installing dependencies..."
# This will install the packages defined in the pyproject.toml file
poetry install

# Sync and remove unnecessary packages
echo "Syncing Poetry environment..."
# This will ensure that the environment matches the pyproject.toml file
# It will also remove any packages that are not listed in the pyproject.toml file
poetry sync

echo "Poetry environment setup complete."
