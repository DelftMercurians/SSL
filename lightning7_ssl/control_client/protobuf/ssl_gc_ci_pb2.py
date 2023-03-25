# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_gc_ci.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_gc_api_pb2 as ssl__gc__api__pb2
import ssl_geometry_pb2 as ssl__geometry__pb2
import ssl_referee_pb2 as ssl__referee__pb2
import ssl_vision_wrapper_tracked_pb2 as ssl__vision__wrapper__tracked__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0fssl_gc_ci.proto\x12\x0egameController\x1a ssl_vision_wrapper_tracked.proto\x1a\x10ssl_gc_api.proto\x1a\x11ssl_referee.proto\x1a\x12ssl_geometry.proto"\xaa\x01\n\x07\x43iInput\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12<\n\x0etracker_packet\x18\x02 \x01(\x0b\x32$.gameController.TrackerWrapperPacket\x12)\n\napi_inputs\x18\x03 \x03(\x0b\x32\x15.gameController.Input\x12#\n\x08geometry\x18\x04 \x01(\x0b\x32\x11.SSL_GeometryData"-\n\x08\x43iOutput\x12!\n\x0breferee_msg\x18\x01 \x01(\x0b\x32\x0c.SSL_Referee'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ssl_gc_ci_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _CIINPUT._serialized_start = 127
    _CIINPUT._serialized_end = 297
    _CIOUTPUT._serialized_start = 299
    _CIOUTPUT._serialized_end = 344
# @@protoc_insertion_point(module_scope)
