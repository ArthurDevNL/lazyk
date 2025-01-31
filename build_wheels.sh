#!/bin/bash

# Set environment variables to ensure compatibility with older toolchains
export CFLAGS="-g0 -O2"
export CXXFLAGS="-g0 -O2"
export LDFLAGS="-Wl,--strip-all"

# Install dependencies and build wheels for each Python version
for PYBIN in /opt/python/cp3*/bin; do
    "${PYBIN}/pip" install poetry pybind11 numpy cython wheel setuptools
    "${PYBIN}/poetry" config virtualenvs.create false
    "${PYBIN}/poetry" install --no-root
    "${PYBIN}/poetry" build -f wheel
done

# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    auditwheel repair "$whl" --plat manylinux2014_x86_64 -w /app/wheelhouse/ || echo "Warning: auditwheel repair failed for $whl"
done 