#!/bin/bash
set -e  # Exit on any error

# Build the Docker image
echo "Building Docker image..."
docker build -t lazyk-builder .

# Create wheelhouse directory if it doesn't exist
mkdir -p wheelhouse

# Build the wheels
echo "Building wheels..."
docker run --rm -v $(pwd):/app lazyk-builder

# List the built wheels
echo "Built wheels:"
ls -l wheelhouse/

echo "Build complete! Wheels are in ./wheelhouse/" 