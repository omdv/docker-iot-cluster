from concurrent import futures
import time
import os
import api_pb2
import api_pb2_grpc
import grpc
import logging

PORT = os.environ['PORT']


class CService(api_pb2_grpc.CalcServiceServicer):

    def Calculate(self, request, context):
        try:
            logging.info("Received {}".format(request.payload))
            value = str(-1.0 * float(request.payload))
        except ValueError:
            logging.info("Cannot parse {} to float".format(request.payload))
            value = str(-1.0)
        time.sleep(2)
        return api_pb2.Response(payload=value)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    api_pb2_grpc.add_CalcServiceServicer_to_server(CService(), server)
    server.add_insecure_port('[::]:{}'.format(PORT))
    server.start()
    try:
        while True:
            time.sleep(7*86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
