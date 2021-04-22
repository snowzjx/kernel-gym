import asyncio
import grpc
import logging
from bcc import BPF
from kernel_gym.service.proto import (
    KernelGymServiceServicer,
    StartBPFRequest,
    StartBPFReply,
    add_KernelGymServiceServicer_to_server,
)


class BPFServiceServicer(KernelGymServiceServicer):
    def __init__(self):
        self._b = None

    def StartBPF(self, request: StartBPFRequest, context) -> StartBPFReply:
        logging.info("Starting BPF ...")
        try:
            b = BPF(text=request.bpf_program)
            self._b = b
            return StartBPFReply(ret_code=0)
        except Exception as e:
            logging.info(str(e))
            return StartBPFReply(ret_code=-1)


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
