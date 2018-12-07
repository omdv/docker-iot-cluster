from concurrent import futures
import time
import os
import api_pb2
import api_pb2_grpc
import grpc
import logging
import numpy as np

PORT = os.environ['PORT']


class CService(api_pb2_grpc.CalcServiceServicer):

    def Calculate(self, request, context):
        logging.debug("Received {}".format(request.payload))
        try:
            times, data = deserialize(request.payload)
            logging.debug("Converted to {}".format(data))
            value = np.mean(data)
        except ValueError:
            logging.error("Cannot parse {}".format(request.payload))
            value = -1.0
        time.sleep(2)
        return api_pb2.Response(payload=str(value))


def deserialize(request):
    values, timeseries = []
    request = request.split(",")
    size = int(request[0])
    try:
        for i in range(size):
            timeseries.append(time.localtime(int(request[i+1])/1e9))
            values.append(float(request[i+1+size]))
    except IndexError:
        logging.error("Mismatch of serial string dimensions")
        timeseries = []
        values = []
    return timeseries, values


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
    logging.basicConfig(level=logging.DEBUG)
    serve()
