# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: userinput.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import command_pb2 as command__pb2
import robot_pb2 as robot__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0fuserinput.proto\x12\x04\x61mun\x1a\x0brobot.proto\x1a\rcommand.proto"e\n\tUserInput\x12*\n\rradio_command\x18\x01 \x03(\x0b\x32\x13.robot.RadioCommand\x12,\n\x0cmove_command\x18\x02 \x03(\x0b\x32\x16.amun.RobotMoveCommandB\x03\xf8\x01\x01'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "userinput_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\370\001\001"
    _USERINPUT._serialized_start = 53
    _USERINPUT._serialized_end = 154
# @@protoc_insertion_point(module_scope)
