# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='api.proto',
  package='kapacitor',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\tapi.proto\x12\tkapacitor\"\x1a\n\x07Request\x12\x0f\n\x07payload\x18\x01 \x01(\t\"\x1b\n\x08Response\x12\x0f\n\x07payload\x18\x01 \x01(\t2E\n\x0b\x43\x61lcService\x12\x36\n\tCalculate\x12\x12.kapacitor.Request\x1a\x13.kapacitor.Response\"\x00\x62\x06proto3')
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='kapacitor.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='kapacitor.Request.payload', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=50,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='kapacitor.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='kapacitor.Response.payload', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=79,
)

DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:kapacitor.Request)
  ))
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'api_pb2'
  # @@protoc_insertion_point(class_scope:kapacitor.Response)
  ))
_sym_db.RegisterMessage(Response)



_CALCSERVICE = _descriptor.ServiceDescriptor(
  name='CalcService',
  full_name='kapacitor.CalcService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=81,
  serialized_end=150,
  methods=[
  _descriptor.MethodDescriptor(
    name='Calculate',
    full_name='kapacitor.CalcService.Calculate',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CALCSERVICE)

DESCRIPTOR.services_by_name['CalcService'] = _CALCSERVICE

# @@protoc_insertion_point(module_scope)
