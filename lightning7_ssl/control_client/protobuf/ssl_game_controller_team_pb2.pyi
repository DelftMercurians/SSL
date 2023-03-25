"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import ssl_game_controller_common_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _AdvantageChoice:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _AdvantageChoiceEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_AdvantageChoice.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    STOP: _AdvantageChoice.ValueType  # 0
    """stop the game"""
    CONTINUE: _AdvantageChoice.ValueType  # 1
    """keep the game running"""

class AdvantageChoice(_AdvantageChoice, metaclass=_AdvantageChoiceEnumTypeWrapper):
    """the current advantage choice of the team
    the choice is valid until another choice is received
    if the team disconnects, the choice is reset to its default (STOP)
    teams may either send their current choice continuously or only on change
    """

STOP: AdvantageChoice.ValueType  # 0
"""stop the game"""
CONTINUE: AdvantageChoice.ValueType  # 1
"""keep the game running"""
global___AdvantageChoice = AdvantageChoice

@typing_extensions.final
class TeamRegistration(google.protobuf.message.Message):
    """a registration that must be send by teams and autoRefs to the controller as the very first message"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TEAM_NAME_FIELD_NUMBER: builtins.int
    SIGNATURE_FIELD_NUMBER: builtins.int
    team_name: builtins.str
    """the exact team name as published by the game-controller"""
    @property
    def signature(self) -> ssl_game_controller_common_pb2.Signature:
        """signature can optionally be specified to enable secure communication"""
    def __init__(
        self,
        *,
        team_name: builtins.str | None = ...,
        signature: ssl_game_controller_common_pb2.Signature | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["signature", b"signature", "team_name", b"team_name"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["signature", b"signature", "team_name", b"team_name"]) -> None: ...

global___TeamRegistration = TeamRegistration

@typing_extensions.final
class TeamToController(google.protobuf.message.Message):
    """wrapper for all messages from a team's computer to the controller"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SIGNATURE_FIELD_NUMBER: builtins.int
    DESIRED_KEEPER_FIELD_NUMBER: builtins.int
    ADVANTAGE_CHOICE_FIELD_NUMBER: builtins.int
    SUBSTITUTE_BOT_FIELD_NUMBER: builtins.int
    PING_FIELD_NUMBER: builtins.int
    @property
    def signature(self) -> ssl_game_controller_common_pb2.Signature:
        """signature can optionally be specified to enable secure communication"""
    desired_keeper: builtins.int
    """request a new desired keeper id
    this is only allowed during STOP and will be rejected otherwise
    """
    advantage_choice: global___AdvantageChoice.ValueType
    """response to an advantage choice request"""
    substitute_bot: builtins.bool
    """request to substitute a robot at the next possibility"""
    ping: builtins.bool
    """send a ping to the GC to test if the connection is still open.
    the value is ignored and a reply is sent back
    """
    def __init__(
        self,
        *,
        signature: ssl_game_controller_common_pb2.Signature | None = ...,
        desired_keeper: builtins.int | None = ...,
        advantage_choice: global___AdvantageChoice.ValueType | None = ...,
        substitute_bot: builtins.bool | None = ...,
        ping: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["advantage_choice", b"advantage_choice", "desired_keeper", b"desired_keeper", "msg", b"msg", "ping", b"ping", "signature", b"signature", "substitute_bot", b"substitute_bot"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["advantage_choice", b"advantage_choice", "desired_keeper", b"desired_keeper", "msg", b"msg", "ping", b"ping", "signature", b"signature", "substitute_bot", b"substitute_bot"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["msg", b"msg"]) -> typing_extensions.Literal["desired_keeper", "advantage_choice", "substitute_bot", "ping"] | None: ...

global___TeamToController = TeamToController

@typing_extensions.final
class ControllerToTeam(google.protobuf.message.Message):
    """wrapper for all messages from controller to a team's computer"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONTROLLER_REPLY_FIELD_NUMBER: builtins.int
    @property
    def controller_reply(self) -> ssl_game_controller_common_pb2.ControllerReply:
        """a reply from the controller"""
    def __init__(
        self,
        *,
        controller_reply: ssl_game_controller_common_pb2.ControllerReply | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["controller_reply", b"controller_reply", "msg", b"msg"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["controller_reply", b"controller_reply", "msg", b"msg"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["msg", b"msg"]) -> typing_extensions.Literal["controller_reply"] | None: ...

global___ControllerToTeam = ControllerToTeam