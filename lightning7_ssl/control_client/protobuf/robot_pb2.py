# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: robot.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0brobot.proto\x12\x05robot"\xa5\x01\n\x0fLimitParameters\x12\x17\n\x0f\x61_speedup_f_max\x18\x01 \x01(\x02\x12\x17\n\x0f\x61_speedup_s_max\x18\x02 \x01(\x02\x12\x19\n\x11\x61_speedup_phi_max\x18\x03 \x01(\x02\x12\x15\n\ra_brake_f_max\x18\x04 \x01(\x02\x12\x15\n\ra_brake_s_max\x18\x05 \x01(\x02\x12\x17\n\x0f\x61_brake_phi_max\x18\x06 \x01(\x02"J\n\x10SimulationLimits\x12\x1b\n\x13\x61_speedup_wheel_max\x18\x01 \x01(\x02\x12\x19\n\x11\x61_brake_wheel_max\x18\x02 \x01(\x02"\x92\x04\n\x05Specs\x12\x12\n\ngeneration\x18\x01 \x02(\r\x12\x0c\n\x04year\x18\x02 \x02(\r\x12\n\n\x02id\x18\x03 \x02(\r\x12)\n\x04type\x18\x13 \x01(\x0e\x32\x1b.robot.Specs.GenerationType\x12\x14\n\x06radius\x18\x04 \x01(\x02:\x04\x30.09\x12\x14\n\x06height\x18\x05 \x01(\x02:\x04\x30.15\x12\x0c\n\x04mass\x18\x06 \x01(\x02\x12\r\n\x05\x61ngle\x18\x07 \x01(\x02\x12\r\n\x05v_max\x18\x08 \x01(\x02\x12\x11\n\tomega_max\x18\t \x01(\x02\x12\x1a\n\x0fshot_linear_max\x18\n \x01(\x02:\x01\x38\x12\x15\n\rshot_chip_max\x18\x0b \x01(\x02\x12\x16\n\x0e\x64ribbler_width\x18\x0c \x01(\x02\x12,\n\x0c\x61\x63\x63\x65leration\x18\r \x01(\x0b\x32\x16.robot.LimitParameters\x12(\n\x08strategy\x18\x10 \x01(\x0b\x32\x16.robot.LimitParameters\x12\x10\n\x08ir_param\x18\x0f \x01(\x02\x12\x14\n\x0cshoot_radius\x18\x11 \x01(\x02\x12\x17\n\x0f\x64ribbler_height\x18\x12 \x01(\x02\x12\x32\n\x11simulation_limits\x18\x15 \x01(\x0b\x32\x17.robot.SimulationLimits"\'\n\x0eGenerationType\x12\x0b\n\x07Regular\x10\x01\x12\x08\n\x04\x41lly\x10\x02J\x04\x08\x14\x10\x15"H\n\nGeneration\x12\x1d\n\x07\x64\x65\x66\x61ult\x18\x01 \x02(\x0b\x32\x0c.robot.Specs\x12\x1b\n\x05robot\x18\x02 \x03(\x0b\x32\x0c.robot.Specs"#\n\x04Team\x12\x1b\n\x05robot\x18\x01 \x03(\x0b\x32\x0c.robot.Specs"<\n\nPolynomial\x12\n\n\x02\x61\x30\x18\x01 \x02(\x02\x12\n\n\x02\x61\x31\x18\x02 \x02(\x02\x12\n\n\x02\x61\x32\x18\x03 \x02(\x02\x12\n\n\x02\x61\x33\x18\x04 \x02(\x02"\x84\x01\n\x06Spline\x12\x0f\n\x07t_start\x18\x01 \x02(\x02\x12\r\n\x05t_end\x18\x02 \x02(\x02\x12\x1c\n\x01x\x18\x03 \x02(\x0b\x32\x11.robot.Polynomial\x12\x1c\n\x01y\x18\x04 \x02(\x0b\x32\x11.robot.Polynomial\x12\x1e\n\x03phi\x18\x05 \x02(\x0b\x32\x11.robot.Polynomial"0\n\x0f\x43ontrollerInput\x12\x1d\n\x06spline\x18\x01 \x03(\x0b\x32\r.robot.Spline"6\n\x0bSpeedVector\x12\x0b\n\x03v_s\x18\x01 \x01(\x02\x12\x0b\n\x03v_f\x18\x02 \x01(\x02\x12\r\n\x05omega\x18\x03 \x01(\x02"\xfc\x03\n\x07\x43ommand\x12*\n\ncontroller\x18\x01 \x01(\x0b\x32\x16.robot.ControllerInput\x12\x0b\n\x03v_f\x18\x02 \x01(\x02\x12\x0b\n\x03v_s\x18\x03 \x01(\x02\x12\r\n\x05omega\x18\x04 \x01(\x02\x12,\n\nkick_style\x18\x05 \x01(\x0e\x32\x18.robot.Command.KickStyle\x12\x12\n\nkick_power\x18\x06 \x01(\x02\x12\x10\n\x08\x64ribbler\x18\x07 \x01(\x02\x12\r\n\x05local\x18\x08 \x01(\x08\x12\x0f\n\x07standby\x18\x0b \x01(\x08\x12\x1b\n\x13strategy_controlled\x18\r \x01(\x08\x12\x12\n\nforce_kick\x18\x0e \x01(\x08\x12\x1a\n\x12network_controlled\x18\x0f \x01(\x08\x12\x14\n\x0c\x65ject_sdcard\x18\x10 \x01(\x08\x12\x0f\n\x07\x63ur_v_f\x18\x11 \x01(\x02\x12\x0f\n\x07\x63ur_v_s\x18\x12 \x01(\x02\x12\x11\n\tcur_omega\x18\x13 \x01(\x02\x12#\n\x07output0\x18\x14 \x01(\x0b\x32\x12.robot.SpeedVector\x12#\n\x07output1\x18\x15 \x01(\x0b\x32\x12.robot.SpeedVector\x12#\n\x07output2\x18\x16 \x01(\x0b\x32\x12.robot.SpeedVector"!\n\tKickStyle\x12\n\n\x06Linear\x10\x01\x12\x08\n\x04\x43hip\x10\x02"v\n\x0cRadioCommand\x12\x12\n\ngeneration\x18\x01 \x02(\r\x12\n\n\x02id\x18\x02 \x02(\r\x12\x0f\n\x07is_blue\x18\x04 \x01(\x08\x12\x1f\n\x07\x63ommand\x18\x03 \x02(\x0b\x32\x0e.robot.Command\x12\x14\n\x0c\x63ommand_time\x18\x05 \x01(\x03"6\n\x0bSpeedStatus\x12\x0b\n\x03v_f\x18\x01 \x02(\x02\x12\x0b\n\x03v_s\x18\x02 \x02(\x02\x12\r\n\x05omega\x18\x03 \x02(\x02"\x87\x02\n\rExtendedError\x12\x15\n\rmotor_1_error\x18\x01 \x02(\x08\x12\x15\n\rmotor_2_error\x18\x02 \x02(\x08\x12\x15\n\rmotor_3_error\x18\x03 \x02(\x08\x12\x15\n\rmotor_4_error\x18\x04 \x02(\x08\x12\x16\n\x0e\x64ribbler_error\x18\x05 \x02(\x08\x12\x14\n\x0ckicker_error\x18\x06 \x02(\x08\x12\x1f\n\x17kicker_break_beam_error\x18\x0b \x01(\x08\x12\x1b\n\x13motor_encoder_error\x18\t \x01(\x08\x12\x19\n\x11main_sensor_error\x18\n \x01(\x08\x12\x13\n\x0btemperature\x18\x07 \x01(\x05"\xc0\x02\n\rRadioResponse\x12\x0c\n\x04time\x18\n \x01(\x03\x12\x12\n\ngeneration\x18\x01 \x02(\r\x12\n\n\x02id\x18\x02 \x02(\r\x12\x0f\n\x07\x62\x61ttery\x18\x03 \x01(\x02\x12\x16\n\x0epacket_loss_rx\x18\x04 \x01(\x02\x12\x16\n\x0epacket_loss_tx\x18\x05 \x01(\x02\x12+\n\x0f\x65stimated_speed\x18\x06 \x01(\x0b\x32\x12.robot.SpeedStatus\x12\x15\n\rball_detected\x18\x07 \x01(\x08\x12\x13\n\x0b\x63\x61p_charged\x18\x08 \x01(\x08\x12\x15\n\rerror_present\x18\t \x01(\x08\x12\x11\n\tradio_rtt\x18\x0b \x01(\x02\x12,\n\x0e\x65xtended_error\x18\x0c \x01(\x0b\x32\x14.robot.ExtendedError\x12\x0f\n\x07is_blue\x18\r \x01(\x08\x42\x03\xf8\x01\x01'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "robot_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\370\001\001"
    _LIMITPARAMETERS._serialized_start = 23
    _LIMITPARAMETERS._serialized_end = 188
    _SIMULATIONLIMITS._serialized_start = 190
    _SIMULATIONLIMITS._serialized_end = 264
    _SPECS._serialized_start = 267
    _SPECS._serialized_end = 797
    _SPECS_GENERATIONTYPE._serialized_start = 752
    _SPECS_GENERATIONTYPE._serialized_end = 791
    _GENERATION._serialized_start = 799
    _GENERATION._serialized_end = 871
    _TEAM._serialized_start = 873
    _TEAM._serialized_end = 908
    _POLYNOMIAL._serialized_start = 910
    _POLYNOMIAL._serialized_end = 970
    _SPLINE._serialized_start = 973
    _SPLINE._serialized_end = 1105
    _CONTROLLERINPUT._serialized_start = 1107
    _CONTROLLERINPUT._serialized_end = 1155
    _SPEEDVECTOR._serialized_start = 1157
    _SPEEDVECTOR._serialized_end = 1211
    _COMMAND._serialized_start = 1214
    _COMMAND._serialized_end = 1722
    _COMMAND_KICKSTYLE._serialized_start = 1689
    _COMMAND_KICKSTYLE._serialized_end = 1722
    _RADIOCOMMAND._serialized_start = 1724
    _RADIOCOMMAND._serialized_end = 1842
    _SPEEDSTATUS._serialized_start = 1844
    _SPEEDSTATUS._serialized_end = 1898
    _EXTENDEDERROR._serialized_start = 1901
    _EXTENDEDERROR._serialized_end = 2164
    _RADIORESPONSE._serialized_start = 2167
    _RADIORESPONSE._serialized_end = 2487
# @@protoc_insertion_point(module_scope)
