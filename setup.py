from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "lazy_k",
        ["src/pybind_module.cpp", "src/lazyk.cpp"],
        include_dirs=["include"],
    ),
]

setup(
    name="lazyk",
    version="0.1.0",
    author="Arthur Hemmer",
    author_email="arthur.hemmer@shift-technology.com.com",
    description="A Python library with a C++ implementation of the lazy-k algorithm",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
