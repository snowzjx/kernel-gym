load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "envs",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":kernel_gym_env",
    ],
)

py_library(
    name = "kernel_gym_env",
    srcs = ["kernel_gym_env.py"],
    visibility = ["//kernel_gym_env:__subpackages__"],
)