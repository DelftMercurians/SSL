# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_vision_wrapper_tracked.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_vision_detection_tracked_pb2 as ssl__vision__detection__tracked__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n ssl_vision_wrapper_tracked.proto\x12\x0egameController\x1a"ssl_vision_detection_tracked.proto"n\n\x14TrackerWrapperPacket\x12\x0c\n\x04uuid\x18\x01 \x02(\t\x12\x13\n\x0bsource_name\x18\x02 \x01(\t\x12\x33\n\rtracked_frame\x18\x03 \x01(\x0b\x32\x1c.gameController.TrackedFrame'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ssl_vision_wrapper_tracked_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _TRACKERWRAPPERPACKET._serialized_start = 88
    _TRACKERWRAPPERPACKET._serialized_end = 198
# @@protoc_insertion_point(module_scope)
