from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
from setuptools import setup, Extension
import pybind11

ext_modules = [
    Pybind11Extension(
        "lazyk",
        [
            "src/lazyk_pybind.cpp",
            "src/lazyk.cpp",
        ],
        include_dirs=[
            "src",
            pybind11.get_include(),
        ],
        language='c++',
        cxx_std=14,
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.10",
) 