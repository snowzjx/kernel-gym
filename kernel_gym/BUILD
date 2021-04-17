load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "kernel_gym",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//kernel_gym/dsl",
        "//kernel_gym/envs",
        "//kernel_gym/service",
        "//kernel_gym/spaces",
        "//kernel_gym/utils",
        "//kernel_gym/views",
    ],
)