import grpc

import api_pb2
import api_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = api_pb2_grpc.CalcServiceStub(channel)
    response = stub.Calculate(api_pb2.Request(payload="123.45"))
    print("Response received:{}".format(response.payload))


if __name__ == "__main__":
    run()
