load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "views",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":observation",
        ":observation_space"
    ],
)

py_library(
    name = "observation",
    srcs = ["observation.py"],
    deps = [
        "//kernel_gym/service",
        "//kernel_gym/service/proto",
    ],
)

py_library(
    name = "observation_space",
    srcs = ["observation_space.py"],
    deps = [
        "//kernel_gym/service",
        "//kernel_gym/service/proto",
    ],
)