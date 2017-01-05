cmake_minimum_required(VERSION 3.1)

project(pybind11-test VERSION 0.1.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(pybind11 REQUIRED)

pybind11_add_module(example example.cpp)
target_link_libraries(example PRIVATE pybind11::module)
