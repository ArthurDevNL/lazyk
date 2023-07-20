#include <pybind11/pybind11.h>  
#include <pybind11/stl.h>  
#include "lazyk.cpp"  
  
namespace py = pybind11;  
  
PYBIND11_MODULE(layzk, m) {  
    py::class_<Lazyk>(m, "Lazyk")  
        .def(py::init<State>())  
        .def("__iter__", [](Lazyk &self) { return self; })  
        .def("__next__", [](Lazyk &self) {  
            if (self.end()) {  
                throw py::stop_iteration();  
            }  
            self.operator++();  
            return self.get_assignment();  
        });  
  
    py::class_<State>(m, "State")  
        .def(py::init<vector<vector<double>>>());  
}  
