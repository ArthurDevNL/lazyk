#!/bin/bash
set -e  # Exit on any error

# Parse command line arguments
IS_TEST=false
if [ "$1" == "--test" ]; then
    IS_TEST=true
fi

# Set credentials based on environment
if [ "$IS_TEST" = true ]; then
    USERNAME="$PYPI_TEST_USERNAME"
    PASSWORD="$PYPI_TEST_PASSWORD"
    REPO="https://test.pypi.org/legacy/"
    echo "Using TestPyPI environment..."
else
    USERNAME="$PYPI_USERNAME"
    PASSWORD="$PYPI_PASSWORD"
    REPO="https://upload.pypi.org/legacy/"
    echo "Using production PyPI environment..."
fi

# Check if credentials are set
if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
    echo "Please set $([ "$IS_TEST" = true ] && echo "PYPI_TEST_USERNAME and PYPI_TEST_PASSWORD" || echo "PYPI_USERNAME and PYPI_PASSWORD") environment variables"
    exit 1
fi

# Install twine if not already installed
pip install --upgrade twine

# Check the distribution files
echo "Checking distribution files..."
twine check wheelhouse/*

# Prompt for confirmation
echo "Ready to upload to PyPI. Please confirm (y/n)"
read -r confirm
if [ "$confirm" != "y" ]; then
    echo "Upload cancelled"
    exit 1
fi

# Upload to PyPI
echo "Uploading to $([ "$IS_TEST" = true ] && echo "TestPyPI" || echo "PyPI")..."
twine upload --repository-url "$REPO" --username "$USERNAME" --password "$PASSWORD" wheelhouse/*

echo "Upload complete!" 