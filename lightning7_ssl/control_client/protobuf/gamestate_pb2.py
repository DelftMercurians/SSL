# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gamestate.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_game_event_2019_pb2 as ssl__game__event__2019__pb2
import ssl_referee_game_event_pb2 as ssl__referee__game__event__pb2
import ssl_referee_pb2 as ssl__referee__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0fgamestate.proto\x12\x04\x61mun\x1a\x11ssl_referee.proto\x1a\x1cssl_referee_game_event.proto\x1a\x19ssl_game_event_2019.proto"\x87\x07\n\tGameState\x12!\n\x05stage\x18\x01 \x02(\x0e\x32\x12.SSL_Referee.Stage\x12\x17\n\x0fstage_time_left\x18\x02 \x01(\x11\x12$\n\x05state\x18\x03 \x02(\x0e\x32\x15.amun.GameState.State\x12%\n\x06yellow\x18\x04 \x02(\x0b\x32\x15.SSL_Referee.TeamInfo\x12#\n\x04\x62lue\x18\x05 \x02(\x0b\x32\x15.SSL_Referee.TeamInfo\x12/\n\x13\x64\x65signated_position\x18\x06 \x01(\x0b\x32\x12.SSL_Referee.Point\x12/\n\ngame_event\x18\x07 \x01(\x0b\x32\x17.SSL_Referee_Game_EventB\x02\x18\x01\x12\x15\n\rgoals_flipped\x18\x08 \x01(\x08\x12\x1c\n\x14is_real_game_running\x18\t \x01(\x08\x12%\n\x1d\x63urrent_action_time_remaining\x18\n \x01(\x05\x12)\n\nnext_state\x18\x0b \x01(\x0e\x32\x15.amun.GameState.State\x12\x32\n\x0fgame_event_2019\x18\x0c \x03(\x0b\x32\x19.gameController.GameEvent"\xae\x03\n\x05State\x12\x08\n\x04Halt\x10\x01\x12\x08\n\x04Stop\x10\x02\x12\x08\n\x04Game\x10\x03\x12\r\n\tGameForce\x10\x04\x12\x18\n\x14KickoffYellowPrepare\x10\x05\x12\x11\n\rKickoffYellow\x10\x06\x12\x18\n\x14PenaltyYellowPrepare\x10\x07\x12\x11\n\rPenaltyYellow\x10\x08\x12\x18\n\x14PenaltyYellowRunning\x10\x15\x12\x10\n\x0c\x44irectYellow\x10\t\x12\x12\n\x0eIndirectYellow\x10\n\x12\x17\n\x13\x42\x61llPlacementYellow\x10\x13\x12\x16\n\x12KickoffBluePrepare\x10\x0b\x12\x0f\n\x0bKickoffBlue\x10\x0c\x12\x16\n\x12PenaltyBluePrepare\x10\r\x12\x0f\n\x0bPenaltyBlue\x10\x0e\x12\x16\n\x12PenaltyBlueRunning\x10\x16\x12\x0e\n\nDirectBlue\x10\x0f\x12\x10\n\x0cIndirectBlue\x10\x10\x12\x15\n\x11\x42\x61llPlacementBlue\x10\x14\x12\x11\n\rTimeoutYellow\x10\x11\x12\x0f\n\x0bTimeoutBlue\x10\x12\x42\x03\xf8\x01\x01'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "gamestate_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\370\001\001"
    _GAMESTATE.fields_by_name["game_event"]._options = None
    _GAMESTATE.fields_by_name["game_event"]._serialized_options = b"\030\001"
    _GAMESTATE._serialized_start = 102
    _GAMESTATE._serialized_end = 1005
    _GAMESTATE_STATE._serialized_start = 575
    _GAMESTATE_STATE._serialized_end = 1005
# @@protoc_insertion_point(module_scope)
