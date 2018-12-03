# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import api_pb2 as api__pb2


class CalcServiceStub(object):
  """service, encode a plain text 
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Calculate = channel.unary_unary(
        '/kapacitor.CalcService/Calculate',
        request_serializer=api__pb2.Request.SerializeToString,
        response_deserializer=api__pb2.Response.FromString,
        )


class CalcServiceServicer(object):
  """service, encode a plain text 
  """

  def Calculate(self, request, context):
    """request a service of encode
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CalcServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Calculate': grpc.unary_unary_rpc_method_handler(
          servicer.Calculate,
          request_deserializer=api__pb2.Request.FromString,
          response_serializer=api__pb2.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'kapacitor.CalcService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
