cmake_minimum_required(VERSION 3.16)
project(hermesengine)
add_subdirectory(BPP Engine)
add_subdirectory(SCP Engine)
add_subdirectory(KBP Engine)
add_subdirectory(KCP Engine)
add_subdirectory(Engine Core)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Project directories
set(PROJECT_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/..")

# Your executable
add_executable(testing
    core/testing.cpp
    core/binary_processing.cpp
    core/constants.cpp
)

# Project headers
target_include_directories(testing PRIVATE
    "${PROJECT_ROOT}/include"
)

# Force the compiler to use your bundled LIEF headers
target_include_directories(testing PRIVATE
    "${PROJECT_ROOT}/dependencies/include"
)
