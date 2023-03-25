# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_referee_game_event.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1cssl_referee_game_event.proto"\x9e\x06\n\x16SSL_Referee_Game_Event\x12<\n\rgameEventType\x18\x01 \x02(\x0e\x32%.SSL_Referee_Game_Event.GameEventType\x12\x36\n\noriginator\x18\x02 \x01(\x0b\x32".SSL_Referee_Game_Event.Originator\x12\x0f\n\x07message\x18\x03 \x01(\t\x1aG\n\nOriginator\x12*\n\x04team\x18\x01 \x02(\x0e\x32\x1c.SSL_Referee_Game_Event.Team\x12\r\n\x05\x62otId\x18\x02 \x01(\r"\xf9\x03\n\rGameEventType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06\x43USTOM\x10\x01\x12\x15\n\x11NUMBER_OF_PLAYERS\x10\x02\x12\x13\n\x0f\x42\x41LL_LEFT_FIELD\x10\x03\x12\x08\n\x04GOAL\x10\x04\x12\x10\n\x0cKICK_TIMEOUT\x10\x05\x12\x17\n\x13NO_PROGRESS_IN_GAME\x10\x06\x12\x11\n\rBOT_COLLISION\x10\x07\x12\x15\n\x11MULTIPLE_DEFENDER\x10\x08\x12\x1f\n\x1bMULTIPLE_DEFENDER_PARTIALLY\x10\t\x12\x1c\n\x18\x41TTACKER_IN_DEFENSE_AREA\x10\n\x12\t\n\x05ICING\x10\x0b\x12\x0e\n\nBALL_SPEED\x10\x0c\x12\x14\n\x10ROBOT_STOP_SPEED\x10\r\x12\x12\n\x0e\x42\x41LL_DRIBBLING\x10\x0e\x12\x19\n\x15\x41TTACKER_TOUCH_KEEPER\x10\x0f\x12\x10\n\x0c\x44OUBLE_TOUCH\x10\x10\x12\x1c\n\x18\x41TTACKER_TO_DEFENCE_AREA\x10\x11\x12#\n\x1f\x44\x45\x46\x45NDER_TO_KICK_POINT_DISTANCE\x10\x12\x12\x10\n\x0c\x42\x41LL_HOLDING\x10\x13\x12\x11\n\rINDIRECT_GOAL\x10\x14\x12\x19\n\x15\x42\x41LL_PLACEMENT_FAILED\x10\x15\x12\x10\n\x0c\x43HIP_ON_GOAL\x10\x16"8\n\x04Team\x12\x10\n\x0cTEAM_UNKNOWN\x10\x00\x12\x0f\n\x0bTEAM_YELLOW\x10\x01\x12\r\n\tTEAM_BLUE\x10\x02'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ssl_referee_game_event_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _SSL_REFEREE_GAME_EVENT._serialized_start = 33
    _SSL_REFEREE_GAME_EVENT._serialized_end = 831
    _SSL_REFEREE_GAME_EVENT_ORIGINATOR._serialized_start = 194
    _SSL_REFEREE_GAME_EVENT_ORIGINATOR._serialized_end = 265
    _SSL_REFEREE_GAME_EVENT_GAMEEVENTTYPE._serialized_start = 268
    _SSL_REFEREE_GAME_EVENT_GAMEEVENTTYPE._serialized_end = 773
    _SSL_REFEREE_GAME_EVENT_TEAM._serialized_start = 775
    _SSL_REFEREE_GAME_EVENT_TEAM._serialized_end = 831
# @@protoc_insertion_point(module_scope)
