load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")

py_library(
    name = "proto",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [":kernel_gym_service_py"],
)

proto_library(
    name = "kernel_gym_service",
    srcs = ["kernel_gym_service.proto"],
    visibility = ["//visibility:public"],
)

py_proto_library(
    name = "kernel_gym_service_py",
    deps = [":kernel_gym_service"],
)