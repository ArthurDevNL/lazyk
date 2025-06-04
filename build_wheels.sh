#!/bin/bash

# Set environment variables to ensure compatibility with older toolchains
export CFLAGS="-g0 -O2"
export CXXFLAGS="-g0 -O2"
export LDFLAGS="-Wl,--strip-all"

# Install dependencies and build wheels for each Python version using uv
for PYBIN in /opt/python/cp3*/bin; do
    # Install uv in the current Python environment
    "${PYBIN}/pip" install uv

    # Install build requirements using this interpreter
    "${PYBIN}/uv" pip install -p "${PYBIN}/python" pybind11 numpy cython wheel setuptools

    # Build wheel with uv
    "${PYBIN}/uv" build --wheel -p "${PYBIN}/python"
done

# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    auditwheel repair "$whl" --plat manylinux2014_x86_64 -w /app/wheelhouse/ || echo "Warning: auditwheel repair failed for $whl"
done
