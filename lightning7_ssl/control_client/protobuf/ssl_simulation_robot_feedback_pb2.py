# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_simulation_robot_feedback.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_simulation_error_pb2 as ssl__simulation__error__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n#ssl_simulation_robot_feedback.proto\x12\x06sslsim\x1a\x1assl_simulation_error.proto\x1a\x19google/protobuf/any.proto"`\n\rRobotFeedback\x12\n\n\x02id\x18\x01 \x02(\r\x12\x1d\n\x15\x64ribbler_ball_contact\x18\x02 \x01(\x08\x12$\n\x06\x63ustom\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any"g\n\x14RobotControlResponse\x12&\n\x06\x65rrors\x18\x01 \x03(\x0b\x32\x16.sslsim.SimulatorError\x12\'\n\x08\x66\x65\x65\x64\x62\x61\x63k\x18\x02 \x03(\x0b\x32\x15.sslsim.RobotFeedback'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ssl_simulation_robot_feedback_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ROBOTFEEDBACK._serialized_start = 102
    _ROBOTFEEDBACK._serialized_end = 198
    _ROBOTCONTROLRESPONSE._serialized_start = 200
    _ROBOTCONTROLRESPONSE._serialized_end = 303
# @@protoc_insertion_point(module_scope)
