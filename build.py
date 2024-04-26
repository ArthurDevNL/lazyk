from glob import glob
from pybind11.setup_helpers import Pybind11Extension, build_ext

def build(setup_kwargs):
    setup_kwargs.update(
        {
            "ext_modules": 
                [Pybind11Extension(
                    "lazyk",
                    ['src/lazyk_pybind.cpp', 'src/lazyk.cpp'],
                    extra_compile_args=['-O3', '-pthread'],
                    language='c++',
                    cxx_std=11
                )],
            "cmd_class": {"build_ext": build_ext},
            "zip_safe": False,
        }
    )
