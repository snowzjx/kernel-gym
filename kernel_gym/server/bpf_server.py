import asyncio
import logging
from typing import Optional

import grpc
from bcc import BPF

from kernel_gym.service.proto import (
    KernelGymServiceServicer,
    StartBPFRequest,
    StartBPFReply,
    StepRequest,
    StepReply,
    add_KernelGymServiceServicer_to_server,
)


class BPFServiceServicer(KernelGymServiceServicer):
    def __init__(self):
        self._b: Optional[BPF] = None
        self.logger = logging.getLogger("compiler_gym.server")
        self.logger.setLevel(logging.INFO)

    def StartBPF(self, request: StartBPFRequest, context) -> StartBPFReply:
        self.logger.info("Installing BPF Program...")
        try:
            self._b = BPF(text=request.bpf_program)
            return StartBPFReply(ret_code=0)
        except Exception as e:
            self.logger.info(str(e))
            return StartBPFReply(ret_code=-1)

    def Step(self, request: StepRequest, context) -> StepReply:
        self.logger.info("Requiring Stepping ...")
        # TODO For test only
        _map = self._b["test"]
        for key in _map.keys():
            self.logger.info(f"Key: {key} and Value: {_map[key]}")
        return StepReply()


async def serve():
    logging.info("Starting server ...")
    server = grpc.aio.server()
    add_KernelGymServiceServicer_to_server(BPFServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
