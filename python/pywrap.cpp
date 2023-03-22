#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "mickey.h"

namespace py = pybind11;

PYBIND11_MODULE(mickey, m) {
    py::class_<Mickey>(m, "Mickey")
        .def(py::init<std::vector<uint8_t>, uint8_t, std::vector<uint8_t>, uint8_t>())
        .def("encrypt", &Mickey::encrypt)
        .def("decrypt", &Mickey::decrypt)
        .def("setIV", &Mickey::setIV)
        .def("setKey", &Mickey::setKey)
        .def("generateKeystreamByte", &Mickey::generateKeystreamByte);
}
