# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_referee.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_game_event_2019_pb2 as ssl__game__event__2019__pb2
import ssl_referee_game_event_pb2 as ssl__referee__game__event__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11ssl_referee.proto\x1a\x1cssl_referee_game_event.proto\x1a\x19ssl_game_event_2019.proto"\xa7\x0e\n\x0bSSL_Referee\x12\x18\n\x10packet_timestamp\x18\x01 \x02(\x04\x12!\n\x05stage\x18\x02 \x02(\x0e\x32\x12.SSL_Referee.Stage\x12\x17\n\x0fstage_time_left\x18\x03 \x01(\x11\x12%\n\x07\x63ommand\x18\x04 \x02(\x0e\x32\x14.SSL_Referee.Command\x12\x17\n\x0f\x63ommand_counter\x18\x05 \x02(\r\x12\x19\n\x11\x63ommand_timestamp\x18\x06 \x02(\x04\x12%\n\x06yellow\x18\x07 \x02(\x0b\x32\x15.SSL_Referee.TeamInfo\x12#\n\x04\x62lue\x18\x08 \x02(\x0b\x32\x15.SSL_Referee.TeamInfo\x12/\n\x13\x64\x65signated_position\x18\t \x01(\x0b\x32\x12.SSL_Referee.Point\x12\x1e\n\x16\x62lueTeamOnPositiveHalf\x18\n \x01(\x08\x12.\n\tgameEvent\x18\x0b \x01(\x0b\x32\x17.SSL_Referee_Game_EventB\x02\x18\x01\x12*\n\x0cnext_command\x18\x0c \x01(\x0e\x32\x14.SSL_Referee.Command\x12\x36\n\x0fgame_events_old\x18\r \x03(\x0b\x32\x19.gameController.GameEventB\x02\x18\x01\x12.\n\x0bgame_events\x18\x10 \x03(\x0b\x32\x19.gameController.GameEvent\x12\x34\n\x14proposed_game_events\x18\x0e \x03(\x0b\x32\x12.ProposedGameEventB\x02\x18\x01\x12\x35\n\x14game_event_proposals\x18\x11 \x03(\x0b\x32\x17.GameEventProposalGroup\x12\x19\n\x11source_identifier\x18\x12 \x01(\t\x12%\n\x1d\x63urrent_action_time_remaining\x18\x0f \x01(\x05\x1a\xda\x02\n\x08TeamInfo\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05score\x18\x02 \x02(\r\x12\x11\n\tred_cards\x18\x03 \x02(\r\x12\x1d\n\x11yellow_card_times\x18\x04 \x03(\rB\x02\x10\x01\x12\x14\n\x0cyellow_cards\x18\x05 \x02(\r\x12\x10\n\x08timeouts\x18\x06 \x02(\r\x12\x14\n\x0ctimeout_time\x18\x07 \x02(\r\x12\x0e\n\x06goalie\x18\x08 \x02(\r\x12\x14\n\x0c\x66oul_counter\x18\t \x01(\r\x12\x1f\n\x17\x62\x61ll_placement_failures\x18\n \x01(\r\x12\x16\n\x0e\x63\x61n_place_ball\x18\x0c \x01(\x08\x12\x18\n\x10max_allowed_bots\x18\r \x01(\r\x12\x1f\n\x17\x62ot_substitution_intent\x18\x0e \x01(\x08\x12\'\n\x1f\x62\x61ll_placement_failures_reached\x18\x0f \x01(\x08\x1a\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02"\xd1\x02\n\x05Stage\x12\x19\n\x15NORMAL_FIRST_HALF_PRE\x10\x00\x12\x15\n\x11NORMAL_FIRST_HALF\x10\x01\x12\x14\n\x10NORMAL_HALF_TIME\x10\x02\x12\x1a\n\x16NORMAL_SECOND_HALF_PRE\x10\x03\x12\x16\n\x12NORMAL_SECOND_HALF\x10\x04\x12\x14\n\x10\x45XTRA_TIME_BREAK\x10\x05\x12\x18\n\x14\x45XTRA_FIRST_HALF_PRE\x10\x06\x12\x14\n\x10\x45XTRA_FIRST_HALF\x10\x07\x12\x13\n\x0f\x45XTRA_HALF_TIME\x10\x08\x12\x19\n\x15\x45XTRA_SECOND_HALF_PRE\x10\t\x12\x15\n\x11\x45XTRA_SECOND_HALF\x10\n\x12\x1a\n\x16PENALTY_SHOOTOUT_BREAK\x10\x0b\x12\x14\n\x10PENALTY_SHOOTOUT\x10\x0c\x12\r\n\tPOST_GAME\x10\r"\x86\x03\n\x07\x43ommand\x12\x08\n\x04HALT\x10\x00\x12\x08\n\x04STOP\x10\x01\x12\x10\n\x0cNORMAL_START\x10\x02\x12\x0f\n\x0b\x46ORCE_START\x10\x03\x12\x1a\n\x16PREPARE_KICKOFF_YELLOW\x10\x04\x12\x18\n\x14PREPARE_KICKOFF_BLUE\x10\x05\x12\x1a\n\x16PREPARE_PENALTY_YELLOW\x10\x06\x12\x18\n\x14PREPARE_PENALTY_BLUE\x10\x07\x12\x16\n\x12\x44IRECT_FREE_YELLOW\x10\x08\x12\x14\n\x10\x44IRECT_FREE_BLUE\x10\t\x12\x18\n\x14INDIRECT_FREE_YELLOW\x10\n\x12\x16\n\x12INDIRECT_FREE_BLUE\x10\x0b\x12\x12\n\x0eTIMEOUT_YELLOW\x10\x0c\x12\x10\n\x0cTIMEOUT_BLUE\x10\r\x12\x0f\n\x0bGOAL_YELLOW\x10\x0e\x12\r\n\tGOAL_BLUE\x10\x0f\x12\x19\n\x15\x42\x41LL_PLACEMENT_YELLOW\x10\x10\x12\x17\n\x13\x42\x41LL_PLACEMENT_BLUE\x10\x11"l\n\x11ProposedGameEvent\x12\x13\n\x0bvalid_until\x18\x01 \x02(\x04\x12\x13\n\x0bproposer_id\x18\x02 \x02(\t\x12-\n\ngame_event\x18\x03 \x02(\x0b\x32\x19.gameController.GameEvent"Y\n\x16GameEventProposalGroup\x12-\n\ngame_event\x18\x01 \x03(\x0b\x32\x19.gameController.GameEvent\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x02 \x01(\x08\x42\x03\xf8\x01\x01'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ssl_referee_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\370\001\001"
    _SSL_REFEREE_TEAMINFO.fields_by_name["yellow_card_times"]._options = None
    _SSL_REFEREE_TEAMINFO.fields_by_name["yellow_card_times"]._serialized_options = b"\020\001"
    _SSL_REFEREE.fields_by_name["gameEvent"]._options = None
    _SSL_REFEREE.fields_by_name["gameEvent"]._serialized_options = b"\030\001"
    _SSL_REFEREE.fields_by_name["game_events_old"]._options = None
    _SSL_REFEREE.fields_by_name["game_events_old"]._serialized_options = b"\030\001"
    _SSL_REFEREE.fields_by_name["proposed_game_events"]._options = None
    _SSL_REFEREE.fields_by_name["proposed_game_events"]._serialized_options = b"\030\001"
    _SSL_REFEREE._serialized_start = 79
    _SSL_REFEREE._serialized_end = 1910
    _SSL_REFEREE_TEAMINFO._serialized_start = 800
    _SSL_REFEREE_TEAMINFO._serialized_end = 1146
    _SSL_REFEREE_POINT._serialized_start = 1148
    _SSL_REFEREE_POINT._serialized_end = 1177
    _SSL_REFEREE_STAGE._serialized_start = 1180
    _SSL_REFEREE_STAGE._serialized_end = 1517
    _SSL_REFEREE_COMMAND._serialized_start = 1520
    _SSL_REFEREE_COMMAND._serialized_end = 1910
    _PROPOSEDGAMEEVENT._serialized_start = 1912
    _PROPOSEDGAMEEVENT._serialized_end = 2020
    _GAMEEVENTPROPOSALGROUP._serialized_start = 2022
    _GAMEEVENTPROPOSALGROUP._serialized_end = 2111
# @@protoc_insertion_point(module_scope)
