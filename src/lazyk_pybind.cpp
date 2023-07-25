#include <pybind11/pybind11.h>  
#include <pybind11/stl.h>  
#include <pybind11/numpy.h>
#include "lazyk.cpp"  
#include <vector>
  
namespace py = pybind11;  

int add(int i, int j) {  
    return i + j;  
}
  
PYBIND11_MODULE(lazyk, m) {  
    py::class_<Lazyk>(m, "Lazyk")  
        .def(py::init<vector<vector<double>>>())  
        .def("__iter__", [](Lazyk &self) { return self; })  
        .def("__next__", [](Lazyk &self) {  
            if (self.end()) {  
                throw py::stop_iteration();  
            }  
            self.operator++();  
            // return self.get_assignment();

            // Convert the vector<int> to NumPy array
            std::vector<int> vec = self.get_assignment();
            py::array_t<int> arr(vec.size());
            std::copy(vec.begin(), vec.end(), arr.mutable_data());
            return arr;
        });  
}  
