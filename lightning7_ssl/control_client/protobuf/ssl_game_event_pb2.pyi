"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Game_Event(google.protobuf.message.Message):
    """a game event that caused a referee command"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _GameEventType:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _GameEventTypeEnumTypeWrapper(
        google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Game_Event._GameEventType.ValueType],
        builtins.type,
    ):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNKNOWN: Game_Event._GameEventType.ValueType  # 0
        """not set"""
        CUSTOM: Game_Event._GameEventType.ValueType  # 1
        """an event that is not listed in this enum yet.
        Give further details in the message below
        """
        NUMBER_OF_PLAYERS: Game_Event._GameEventType.ValueType  # 2
        """Law 3: Number of players"""
        BALL_LEFT_FIELD: Game_Event._GameEventType.ValueType  # 3
        """Law 9: Ball out of play"""
        GOAL: Game_Event._GameEventType.ValueType  # 4
        """Law 10: Team scored a goal"""
        KICK_TIMEOUT: Game_Event._GameEventType.ValueType  # 5
        """Law 9.3: lack of progress while bringing the ball into play"""
        NO_PROGRESS_IN_GAME: Game_Event._GameEventType.ValueType  # 6
        """Law ?: There is no progress in game for (10|15)? seconds"""
        BOT_COLLISION: Game_Event._GameEventType.ValueType  # 7
        """Law 12: Pushing / Substantial Contact"""
        MULTIPLE_DEFENDER: Game_Event._GameEventType.ValueType  # 8
        """Law 12.2: Defender is completely inside penalty area"""
        MULTIPLE_DEFENDER_PARTIALLY: Game_Event._GameEventType.ValueType  # 9
        """Law 12: Defender is partially inside penalty area"""
        ATTACKER_IN_DEFENSE_AREA: Game_Event._GameEventType.ValueType  # 10
        """Law 12.3: Attacker in defense area"""
        ICING: Game_Event._GameEventType.ValueType  # 11
        """Law 12: Icing (kicking over midline and opponent goal line)"""
        BALL_SPEED: Game_Event._GameEventType.ValueType  # 12
        """Law 12: Ball speed"""
        ROBOT_STOP_SPEED: Game_Event._GameEventType.ValueType  # 13
        """Law 12: Robot speed during STOP"""
        BALL_DRIBBLING: Game_Event._GameEventType.ValueType  # 14
        """Law 12: Maximum dribbling distance"""
        ATTACKER_TOUCH_KEEPER: Game_Event._GameEventType.ValueType  # 15
        """Law 12: Touching the opponent goalkeeper"""
        DOUBLE_TOUCH: Game_Event._GameEventType.ValueType  # 16
        """Law 12: Double touch"""
        ATTACKER_TO_DEFENCE_AREA: Game_Event._GameEventType.ValueType  # 17
        """Law 13-17: Attacker not too close to the opponent's penalty area when ball enters play"""
        DEFENDER_TO_KICK_POINT_DISTANCE: Game_Event._GameEventType.ValueType  # 18
        """Law 13-17: Keeping the correct distance to the ball during opponents freekicks"""
        BALL_HOLDING: Game_Event._GameEventType.ValueType  # 19
        """Law 12: A robot holds the ball deliberately"""
        INDIRECT_GOAL: Game_Event._GameEventType.ValueType  # 20
        """Law 12: The ball entered the goal directly after an indirect kick was performed"""
        BALL_PLACEMENT_FAILED: Game_Event._GameEventType.ValueType  # 21
        """Law 9.2: Ball placement"""
        CHIP_ON_GOAL: Game_Event._GameEventType.ValueType  # 22
        """Law 10: A goal is only scored if the ball has not exceeded a robot height (150mm) between the last
        kick of an attacker and the time the ball crossed the goal line.
        """

    class GameEventType(_GameEventType, metaclass=_GameEventTypeEnumTypeWrapper): ...
    UNKNOWN: Game_Event.GameEventType.ValueType  # 0
    """not set"""
    CUSTOM: Game_Event.GameEventType.ValueType  # 1
    """an event that is not listed in this enum yet.
    Give further details in the message below
    """
    NUMBER_OF_PLAYERS: Game_Event.GameEventType.ValueType  # 2
    """Law 3: Number of players"""
    BALL_LEFT_FIELD: Game_Event.GameEventType.ValueType  # 3
    """Law 9: Ball out of play"""
    GOAL: Game_Event.GameEventType.ValueType  # 4
    """Law 10: Team scored a goal"""
    KICK_TIMEOUT: Game_Event.GameEventType.ValueType  # 5
    """Law 9.3: lack of progress while bringing the ball into play"""
    NO_PROGRESS_IN_GAME: Game_Event.GameEventType.ValueType  # 6
    """Law ?: There is no progress in game for (10|15)? seconds"""
    BOT_COLLISION: Game_Event.GameEventType.ValueType  # 7
    """Law 12: Pushing / Substantial Contact"""
    MULTIPLE_DEFENDER: Game_Event.GameEventType.ValueType  # 8
    """Law 12.2: Defender is completely inside penalty area"""
    MULTIPLE_DEFENDER_PARTIALLY: Game_Event.GameEventType.ValueType  # 9
    """Law 12: Defender is partially inside penalty area"""
    ATTACKER_IN_DEFENSE_AREA: Game_Event.GameEventType.ValueType  # 10
    """Law 12.3: Attacker in defense area"""
    ICING: Game_Event.GameEventType.ValueType  # 11
    """Law 12: Icing (kicking over midline and opponent goal line)"""
    BALL_SPEED: Game_Event.GameEventType.ValueType  # 12
    """Law 12: Ball speed"""
    ROBOT_STOP_SPEED: Game_Event.GameEventType.ValueType  # 13
    """Law 12: Robot speed during STOP"""
    BALL_DRIBBLING: Game_Event.GameEventType.ValueType  # 14
    """Law 12: Maximum dribbling distance"""
    ATTACKER_TOUCH_KEEPER: Game_Event.GameEventType.ValueType  # 15
    """Law 12: Touching the opponent goalkeeper"""
    DOUBLE_TOUCH: Game_Event.GameEventType.ValueType  # 16
    """Law 12: Double touch"""
    ATTACKER_TO_DEFENCE_AREA: Game_Event.GameEventType.ValueType  # 17
    """Law 13-17: Attacker not too close to the opponent's penalty area when ball enters play"""
    DEFENDER_TO_KICK_POINT_DISTANCE: Game_Event.GameEventType.ValueType  # 18
    """Law 13-17: Keeping the correct distance to the ball during opponents freekicks"""
    BALL_HOLDING: Game_Event.GameEventType.ValueType  # 19
    """Law 12: A robot holds the ball deliberately"""
    INDIRECT_GOAL: Game_Event.GameEventType.ValueType  # 20
    """Law 12: The ball entered the goal directly after an indirect kick was performed"""
    BALL_PLACEMENT_FAILED: Game_Event.GameEventType.ValueType  # 21
    """Law 9.2: Ball placement"""
    CHIP_ON_GOAL: Game_Event.GameEventType.ValueType  # 22
    """Law 10: A goal is only scored if the ball has not exceeded a robot height (150mm) between the last
    kick of an attacker and the time the ball crossed the goal line.
    """

    class _Team:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TeamEnumTypeWrapper(
        google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Game_Event._Team.ValueType], builtins.type
    ):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        TEAM_UNKNOWN: Game_Event._Team.ValueType  # 0
        TEAM_YELLOW: Game_Event._Team.ValueType  # 1
        TEAM_BLUE: Game_Event._Team.ValueType  # 2

    class Team(_Team, metaclass=_TeamEnumTypeWrapper):
        """a team"""

    TEAM_UNKNOWN: Game_Event.Team.ValueType  # 0
    TEAM_YELLOW: Game_Event.Team.ValueType  # 1
    TEAM_BLUE: Game_Event.Team.ValueType  # 2

    @typing_extensions.final
    class Originator(google.protobuf.message.Message):
        """information about an originator"""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        TEAM_FIELD_NUMBER: builtins.int
        BOTID_FIELD_NUMBER: builtins.int
        team: global___Game_Event.Team.ValueType
        botId: builtins.int
        def __init__(
            self,
            *,
            team: global___Game_Event.Team.ValueType | None = ...,
            botId: builtins.int | None = ...,
        ) -> None: ...
        def HasField(
            self, field_name: typing_extensions.Literal["botId", b"botId", "team", b"team"]
        ) -> builtins.bool: ...
        def ClearField(
            self, field_name: typing_extensions.Literal["botId", b"botId", "team", b"team"]
        ) -> None: ...

    GAMEEVENTTYPE_FIELD_NUMBER: builtins.int
    ORIGINATOR_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    gameEventType: global___Game_Event.GameEventType.ValueType
    """the game event type that happened"""
    @property
    def originator(self) -> global___Game_Event.Originator:
        """the team and optionally a designated robot that is the originator of the game event"""
    message: builtins.str
    """a message describing further details of this game event"""
    def __init__(
        self,
        *,
        gameEventType: global___Game_Event.GameEventType.ValueType | None = ...,
        originator: global___Game_Event.Originator | None = ...,
        message: builtins.str | None = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "gameEventType", b"gameEventType", "message", b"message", "originator", b"originator"
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "gameEventType", b"gameEventType", "message", b"message", "originator", b"originator"
        ],
    ) -> None: ...

global___Game_Event = Game_Event
