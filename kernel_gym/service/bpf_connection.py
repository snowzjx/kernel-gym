from typing import TypeVar, Protocol
import logging
import grpc

from kernel_gym.service.proto import KernelGymServiceStub

Request = TypeVar("Request")
Reply = TypeVar("Reply")


class StubMethod(Protocol):
    def __call__(
            self, a: Request, timeout: float
    ) -> Reply:
        ...


class BPFConnection(object):
    def __init__(
            self,
            endpoint: str,
            logger: logging.Logger = None,
    ):
        self.channel = grpc.insecure_channel(endpoint)
        self.stub = KernelGymServiceStub(self.channel)
        self.logger = logger or logging.getLogger("compiler_gym.connection")

    def close(self):
        self.channel.close()

    def __call__(
            self,
            stub_method: StubMethod,
            request: Request,
            timeout: float = 60,
    ) -> Reply:
        try:
            return stub_method(request, timeout=timeout)
        except ValueError as e:
            # TODO exception handler
            raise e
        except grpc.RpcError as e:
            # TODO exception handler
            raise e
