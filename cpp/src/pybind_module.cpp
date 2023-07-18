#include <pybind11/pybind11.h>  
#include <pybind11/stl.h>  
#include "lazyk/lazyk.hpp"  
  
namespace py = pybind11;  
  
PYBIND11_MODULE(lazy_k, m) {  
    py::class_<State>(m, "State")  
        .def(py::init<>())  
        .def_readwrite("property", &State::property);  
  
    py::class_<Generator>(m, "Generator")  
        .def(py::init<>())  
        .def("next", &Generator::next)  
        .def("__iter__", [](const Generator &g) { return g; });  
}  
