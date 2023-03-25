# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ssl_gc_change.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ssl_game_controller_common_pb2 as ssl__game__controller__common__pb2
import ssl_game_controller_geometry_pb2 as ssl__game__controller__geometry__pb2
import ssl_game_event_2019_pb2 as ssl__game__event__2019__pb2
import ssl_gc_state_pb2 as ssl__gc__state__pb2
import ssl_referee_pb2 as ssl__referee__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13ssl_gc_change.proto\x12\x0egameController\x1a\x12ssl_gc_state.proto\x1a ssl_game_controller_common.proto\x1a"ssl_game_controller_geometry.proto\x1a\x19ssl_game_event_2019.proto\x1a\x11ssl_referee.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xc0\x01\n\x0bStateChange\x12\n\n\x02id\x18\x01 \x01(\x05\x12(\n\tstate_pre\x18\x02 \x01(\x0b\x32\x15.gameController.State\x12$\n\x05state\x18\x03 \x01(\x0b\x32\x15.gameController.State\x12&\n\x06\x63hange\x18\x04 \x01(\x0b\x32\x16.gameController.Change\x12-\n\ttimestamp\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp"\x89\x08\n\x06\x43hange\x12\x0e\n\x06origin\x18\x01 \x01(\t\x12\x12\n\nrevertible\x18\x10 \x01(\x08\x12\x31\n\x0bnew_command\x18\x02 \x01(\x0b\x32\x1a.gameController.NewCommandH\x00\x12\x33\n\x0c\x63hange_stage\x18\x03 \x01(\x0b\x32\x1b.gameController.ChangeStageH\x00\x12\x45\n\x16set_ball_placement_pos\x18\x04 \x01(\x0b\x32#.gameController.SetBallPlacementPosH\x00\x12\x38\n\x0f\x61\x64\x64_yellow_card\x18\x05 \x01(\x0b\x32\x1d.gameController.AddYellowCardH\x00\x12\x32\n\x0c\x61\x64\x64_red_card\x18\x06 \x01(\x0b\x32\x1a.gameController.AddRedCardH\x00\x12:\n\x10yellow_card_over\x18\x07 \x01(\x0b\x32\x1e.gameController.YellowCardOverH\x00\x12\x36\n\x0e\x61\x64\x64_game_event\x18\x08 \x01(\x0b\x32\x1c.gameController.AddGameEventH\x00\x12\x45\n\x16\x61\x64\x64_passive_game_event\x18\x13 \x01(\x0b\x32#.gameController.AddPassiveGameEventH\x00\x12\x33\n\x0c\x61\x64\x64_proposal\x18\t \x01(\x0b\x32\x1b.gameController.AddProposalH\x00\x12\x42\n\x14start_ball_placement\x18\n \x01(\x0b\x32".gameController.StartBallPlacementH\x00\x12,\n\x08\x63ontinue\x18\x0b \x01(\x0b\x32\x18.gameController.ContinueH\x00\x12\x35\n\rupdate_config\x18\x0c \x01(\x0b\x32\x1c.gameController.UpdateConfigH\x00\x12<\n\x11update_team_state\x18\r \x01(\x0b\x32\x1f.gameController.UpdateTeamStateH\x00\x12\x35\n\rswitch_colors\x18\x0e \x01(\x0b\x32\x1c.gameController.SwitchColorsH\x00\x12(\n\x06revert\x18\x0f \x01(\x0b\x32\x16.gameController.RevertH\x00\x12\x36\n\x0enew_game_state\x18\x11 \x01(\x0b\x32\x1c.gameController.NewGameStateH\x00\x12\x44\n\x15\x61\x63\x63\x65pt_proposal_group\x18\x12 \x01(\x0b\x32#.gameController.AcceptProposalGroupH\x00\x42\x08\n\x06\x63hange"6\n\nNewCommand\x12(\n\x07\x63ommand\x18\x01 \x01(\x0b\x32\x17.gameController.Command"4\n\x0b\x43hangeStage\x12%\n\tnew_stage\x18\x01 \x01(\x0e\x32\x12.SSL_Referee.Stage";\n\x13SetBallPlacementPos\x12$\n\x03pos\x18\x01 \x01(\x0b\x32\x17.gameController.Vector2"p\n\rAddYellowCard\x12&\n\x08\x66or_team\x18\x01 \x01(\x0e\x32\x14.gameController.Team\x12\x37\n\x14\x63\x61used_by_game_event\x18\x02 \x01(\x0b\x32\x19.gameController.GameEvent"m\n\nAddRedCard\x12&\n\x08\x66or_team\x18\x01 \x01(\x0e\x32\x14.gameController.Team\x12\x37\n\x14\x63\x61used_by_game_event\x18\x02 \x01(\x0b\x32\x19.gameController.GameEvent"8\n\x0eYellowCardOver\x12&\n\x08\x66or_team\x18\x01 \x01(\x0e\x32\x14.gameController.Team"=\n\x0c\x41\x64\x64GameEvent\x12-\n\ngame_event\x18\x01 \x01(\x0b\x32\x19.gameController.GameEvent"D\n\x13\x41\x64\x64PassiveGameEvent\x12-\n\ngame_event\x18\x01 \x01(\x0b\x32\x19.gameController.GameEvent"9\n\x0b\x41\x64\x64Proposal\x12*\n\x08proposal\x18\x01 \x01(\x0b\x32\x18.gameController.Proposal"<\n\x13\x41\x63\x63\x65ptProposalGroup\x12\x10\n\x08group_id\x18\x01 \x01(\r\x12\x13\n\x0b\x61\x63\x63\x65pted_by\x18\x02 \x01(\t"\x14\n\x12StartBallPlacement"\n\n\x08\x43ontinue"\x83\x01\n\x0cUpdateConfig\x12*\n\x08\x64ivision\x18\x01 \x01(\x0e\x32\x18.gameController.Division\x12\x30\n\x12\x66irst_kickoff_team\x18\x02 \x01(\x0e\x32\x14.gameController.Team\x12\x15\n\rauto_continue\x18\x03 \x01(\x08"\xd6\x04\n\x0fUpdateTeamState\x12&\n\x08\x66or_team\x18\x01 \x01(\x0e\x32\x14.gameController.Team\x12\x11\n\tteam_name\x18\x02 \x01(\t\x12\r\n\x05goals\x18\x03 \x01(\x05\x12\x12\n\ngoalkeeper\x18\x04 \x01(\x05\x12\x15\n\rtimeouts_left\x18\x05 \x01(\x05\x12\x19\n\x11timeout_time_left\x18\x06 \x01(\t\x12\x18\n\x10on_positive_half\x18\x07 \x01(\x08\x12\x1f\n\x17\x62\x61ll_placement_failures\x18\x08 \x01(\x05\x12\x16\n\x0e\x63\x61n_place_ball\x18\t \x01(\x08\x12\x1c\n\x14\x63hallenge_flags_left\x18\x15 \x01(\x05\x12!\n\x19requests_bot_substitution\x18\n \x01(\x08\x12\x18\n\x10requests_timeout\x18\x11 \x01(\x08\x12\x1a\n\x12requests_challenge\x18\x12 \x01(\x08\x12\x1f\n\x17requests_emergency_stop\x18\x13 \x01(\x08\x12/\n\x0byellow_card\x18\x14 \x01(\x0b\x32\x1a.gameController.YellowCard\x12)\n\x08red_card\x18\x0c \x01(\x0b\x32\x17.gameController.RedCard\x12"\n\x04\x66oul\x18\r \x01(\x0b\x32\x14.gameController.Foul\x12\x1a\n\x12remove_yellow_card\x18\x0e \x01(\r\x12\x17\n\x0fremove_red_card\x18\x0f \x01(\r\x12\x13\n\x0bremove_foul\x18\x10 \x01(\r"\x0e\n\x0cSwitchColors"\x1b\n\x06Revert\x12\x11\n\tchange_id\x18\x01 \x01(\x05"=\n\x0cNewGameState\x12-\n\ngame_state\x18\x01 \x01(\x0b\x32\x19.gameController.GameState'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ssl_gc_change_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _STATECHANGE._serialized_start = 209
    _STATECHANGE._serialized_end = 401
    _CHANGE._serialized_start = 404
    _CHANGE._serialized_end = 1437
    _NEWCOMMAND._serialized_start = 1439
    _NEWCOMMAND._serialized_end = 1493
    _CHANGESTAGE._serialized_start = 1495
    _CHANGESTAGE._serialized_end = 1547
    _SETBALLPLACEMENTPOS._serialized_start = 1549
    _SETBALLPLACEMENTPOS._serialized_end = 1608
    _ADDYELLOWCARD._serialized_start = 1610
    _ADDYELLOWCARD._serialized_end = 1722
    _ADDREDCARD._serialized_start = 1724
    _ADDREDCARD._serialized_end = 1833
    _YELLOWCARDOVER._serialized_start = 1835
    _YELLOWCARDOVER._serialized_end = 1891
    _ADDGAMEEVENT._serialized_start = 1893
    _ADDGAMEEVENT._serialized_end = 1954
    _ADDPASSIVEGAMEEVENT._serialized_start = 1956
    _ADDPASSIVEGAMEEVENT._serialized_end = 2024
    _ADDPROPOSAL._serialized_start = 2026
    _ADDPROPOSAL._serialized_end = 2083
    _ACCEPTPROPOSALGROUP._serialized_start = 2085
    _ACCEPTPROPOSALGROUP._serialized_end = 2145
    _STARTBALLPLACEMENT._serialized_start = 2147
    _STARTBALLPLACEMENT._serialized_end = 2167
    _CONTINUE._serialized_start = 2169
    _CONTINUE._serialized_end = 2179
    _UPDATECONFIG._serialized_start = 2182
    _UPDATECONFIG._serialized_end = 2313
    _UPDATETEAMSTATE._serialized_start = 2316
    _UPDATETEAMSTATE._serialized_end = 2914
    _SWITCHCOLORS._serialized_start = 2916
    _SWITCHCOLORS._serialized_end = 2930
    _REVERT._serialized_start = 2932
    _REVERT._serialized_end = 2959
    _NEWGAMESTATE._serialized_start = 2961
    _NEWGAMESTATE._serialized_end = 3022
# @@protoc_insertion_point(module_scope)
