#!/bin/bash

# Install dependencies and build wheels for each Python version
for PYBIN in /opt/python/cp3*/bin; do
    "${PYBIN}/pip" install poetry pybind11 numpy cython wheel setuptools
    "${PYBIN}/poetry" config virtualenvs.create false
    "${PYBIN}/poetry" install --no-root
    "${PYBIN}/poetry" build -f wheel
done

# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    auditwheel repair "$whl" --plat manylinux2014_x86_64 -w /app/wheelhouse/
done 