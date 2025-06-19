#!/bin/bash
set -e  # Exit on any error

# Parse command line arguments
IS_TEST=false
if [ "$1" == "--test" ]; then
    IS_TEST=true
fi

# Set token based on environment
if [ "$IS_TEST" = true ]; then
    TOKEN="$PYPI_TEST_TOKEN"
    REPO="https://test.pypi.org/legacy/"
    echo "Using TestPyPI environment..."
else
    TOKEN="$PYPI_TOKEN"
    REPO="https://upload.pypi.org/legacy/"
    echo "Using production PyPI environment..."
fi

# Check if token is set
if [ -z "$TOKEN" ]; then
    echo "Please set $([ "$IS_TEST" = true ] && echo "PYPI_TEST_TOKEN" || echo "PYPI_TOKEN") environment variable"
    exit 1
fi

# Install twine if not already installed
uv pip install --upgrade twine

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

# Upload to PyPI using API token
echo "Uploading to $([ "$IS_TEST" = true ] && echo "TestPyPI" || echo "PyPI")..."
twine upload --repository-url "$REPO" --username "__token__" --password "$TOKEN" wheelhouse/*

echo "Upload complete!" 