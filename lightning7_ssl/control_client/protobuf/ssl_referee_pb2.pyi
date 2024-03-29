"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import ssl_game_event_2019_pb2
import ssl_referee_game_event_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class SSL_Referee(google.protobuf.message.Message):
    """Each UDP packet contains one of these messages."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Stage:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StageEnumTypeWrapper(
        google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SSL_Referee._Stage.ValueType],
        builtins.type,
    ):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        NORMAL_FIRST_HALF_PRE: SSL_Referee._Stage.ValueType  # 0
        """The first half is about to start.
        A kickoff is called within this stage.
        This stage ends with the NORMAL_START.
        """
        NORMAL_FIRST_HALF: SSL_Referee._Stage.ValueType  # 1
        """The first half of the normal game, before half time."""
        NORMAL_HALF_TIME: SSL_Referee._Stage.ValueType  # 2
        """Half time between first and second halves."""
        NORMAL_SECOND_HALF_PRE: SSL_Referee._Stage.ValueType  # 3
        """The second half is about to start.
        A kickoff is called within this stage.
        This stage ends with the NORMAL_START.
        """
        NORMAL_SECOND_HALF: SSL_Referee._Stage.ValueType  # 4
        """The second half of the normal game, after half time."""
        EXTRA_TIME_BREAK: SSL_Referee._Stage.ValueType  # 5
        """The break before extra time."""
        EXTRA_FIRST_HALF_PRE: SSL_Referee._Stage.ValueType  # 6
        """The first half of extra time is about to start.
        A kickoff is called within this stage.
        This stage ends with the NORMAL_START.
        """
        EXTRA_FIRST_HALF: SSL_Referee._Stage.ValueType  # 7
        """The first half of extra time."""
        EXTRA_HALF_TIME: SSL_Referee._Stage.ValueType  # 8
        """Half time between first and second extra halves."""
        EXTRA_SECOND_HALF_PRE: SSL_Referee._Stage.ValueType  # 9
        """The second half of extra time is about to start.
        A kickoff is called within this stage.
        This stage ends with the NORMAL_START.
        """
        EXTRA_SECOND_HALF: SSL_Referee._Stage.ValueType  # 10
        """The second half of extra time."""
        PENALTY_SHOOTOUT_BREAK: SSL_Referee._Stage.ValueType  # 11
        """The break before penalty shootout."""
        PENALTY_SHOOTOUT: SSL_Referee._Stage.ValueType  # 12
        """The penalty shootout."""
        POST_GAME: SSL_Referee._Stage.ValueType  # 13
        """The game is over."""

    class Stage(_Stage, metaclass=_StageEnumTypeWrapper):
        """These are the "coarse" stages of the game."""

    NORMAL_FIRST_HALF_PRE: SSL_Referee.Stage.ValueType  # 0
    """The first half is about to start.
    A kickoff is called within this stage.
    This stage ends with the NORMAL_START.
    """
    NORMAL_FIRST_HALF: SSL_Referee.Stage.ValueType  # 1
    """The first half of the normal game, before half time."""
    NORMAL_HALF_TIME: SSL_Referee.Stage.ValueType  # 2
    """Half time between first and second halves."""
    NORMAL_SECOND_HALF_PRE: SSL_Referee.Stage.ValueType  # 3
    """The second half is about to start.
    A kickoff is called within this stage.
    This stage ends with the NORMAL_START.
    """
    NORMAL_SECOND_HALF: SSL_Referee.Stage.ValueType  # 4
    """The second half of the normal game, after half time."""
    EXTRA_TIME_BREAK: SSL_Referee.Stage.ValueType  # 5
    """The break before extra time."""
    EXTRA_FIRST_HALF_PRE: SSL_Referee.Stage.ValueType  # 6
    """The first half of extra time is about to start.
    A kickoff is called within this stage.
    This stage ends with the NORMAL_START.
    """
    EXTRA_FIRST_HALF: SSL_Referee.Stage.ValueType  # 7
    """The first half of extra time."""
    EXTRA_HALF_TIME: SSL_Referee.Stage.ValueType  # 8
    """Half time between first and second extra halves."""
    EXTRA_SECOND_HALF_PRE: SSL_Referee.Stage.ValueType  # 9
    """The second half of extra time is about to start.
    A kickoff is called within this stage.
    This stage ends with the NORMAL_START.
    """
    EXTRA_SECOND_HALF: SSL_Referee.Stage.ValueType  # 10
    """The second half of extra time."""
    PENALTY_SHOOTOUT_BREAK: SSL_Referee.Stage.ValueType  # 11
    """The break before penalty shootout."""
    PENALTY_SHOOTOUT: SSL_Referee.Stage.ValueType  # 12
    """The penalty shootout."""
    POST_GAME: SSL_Referee.Stage.ValueType  # 13
    """The game is over."""

    class _Command:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _CommandEnumTypeWrapper(
        google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SSL_Referee._Command.ValueType],
        builtins.type,
    ):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        HALT: SSL_Referee._Command.ValueType  # 0
        """All robots should completely stop moving."""
        STOP: SSL_Referee._Command.ValueType  # 1
        """Robots must keep 50 cm from the ball."""
        NORMAL_START: SSL_Referee._Command.ValueType  # 2
        """A prepared kickoff or penalty may now be taken."""
        FORCE_START: SSL_Referee._Command.ValueType  # 3
        """The ball is dropped and free for either team."""
        PREPARE_KICKOFF_YELLOW: SSL_Referee._Command.ValueType  # 4
        """The yellow team may move into kickoff position."""
        PREPARE_KICKOFF_BLUE: SSL_Referee._Command.ValueType  # 5
        """The blue team may move into kickoff position."""
        PREPARE_PENALTY_YELLOW: SSL_Referee._Command.ValueType  # 6
        """The yellow team may move into penalty position."""
        PREPARE_PENALTY_BLUE: SSL_Referee._Command.ValueType  # 7
        """The blue team may move into penalty position."""
        DIRECT_FREE_YELLOW: SSL_Referee._Command.ValueType  # 8
        """The yellow team may take a direct free kick."""
        DIRECT_FREE_BLUE: SSL_Referee._Command.ValueType  # 9
        """The blue team may take a direct free kick."""
        INDIRECT_FREE_YELLOW: SSL_Referee._Command.ValueType  # 10
        """The yellow team may take an indirect free kick."""
        INDIRECT_FREE_BLUE: SSL_Referee._Command.ValueType  # 11
        """The blue team may take an indirect free kick."""
        TIMEOUT_YELLOW: SSL_Referee._Command.ValueType  # 12
        """The yellow team is currently in a timeout."""
        TIMEOUT_BLUE: SSL_Referee._Command.ValueType  # 13
        """The blue team is currently in a timeout."""
        GOAL_YELLOW: SSL_Referee._Command.ValueType  # 14
        """The yellow team just scored a goal.
        For information only.
        For rules compliance, teams must treat as STOP.
        """
        GOAL_BLUE: SSL_Referee._Command.ValueType  # 15
        """The blue team just scored a goal."""
        BALL_PLACEMENT_YELLOW: SSL_Referee._Command.ValueType  # 16
        """Equivalent to STOP, but the yellow team must pick up the ball and
        drop it in the Designated Position.
        """
        BALL_PLACEMENT_BLUE: SSL_Referee._Command.ValueType  # 17
        """Equivalent to STOP, but the blue team must pick up the ball and drop
        it in the Designated Position.
        """

    class Command(_Command, metaclass=_CommandEnumTypeWrapper):
        """These are the "fine" states of play on the field."""

    HALT: SSL_Referee.Command.ValueType  # 0
    """All robots should completely stop moving."""
    STOP: SSL_Referee.Command.ValueType  # 1
    """Robots must keep 50 cm from the ball."""
    NORMAL_START: SSL_Referee.Command.ValueType  # 2
    """A prepared kickoff or penalty may now be taken."""
    FORCE_START: SSL_Referee.Command.ValueType  # 3
    """The ball is dropped and free for either team."""
    PREPARE_KICKOFF_YELLOW: SSL_Referee.Command.ValueType  # 4
    """The yellow team may move into kickoff position."""
    PREPARE_KICKOFF_BLUE: SSL_Referee.Command.ValueType  # 5
    """The blue team may move into kickoff position."""
    PREPARE_PENALTY_YELLOW: SSL_Referee.Command.ValueType  # 6
    """The yellow team may move into penalty position."""
    PREPARE_PENALTY_BLUE: SSL_Referee.Command.ValueType  # 7
    """The blue team may move into penalty position."""
    DIRECT_FREE_YELLOW: SSL_Referee.Command.ValueType  # 8
    """The yellow team may take a direct free kick."""
    DIRECT_FREE_BLUE: SSL_Referee.Command.ValueType  # 9
    """The blue team may take a direct free kick."""
    INDIRECT_FREE_YELLOW: SSL_Referee.Command.ValueType  # 10
    """The yellow team may take an indirect free kick."""
    INDIRECT_FREE_BLUE: SSL_Referee.Command.ValueType  # 11
    """The blue team may take an indirect free kick."""
    TIMEOUT_YELLOW: SSL_Referee.Command.ValueType  # 12
    """The yellow team is currently in a timeout."""
    TIMEOUT_BLUE: SSL_Referee.Command.ValueType  # 13
    """The blue team is currently in a timeout."""
    GOAL_YELLOW: SSL_Referee.Command.ValueType  # 14
    """The yellow team just scored a goal.
    For information only.
    For rules compliance, teams must treat as STOP.
    """
    GOAL_BLUE: SSL_Referee.Command.ValueType  # 15
    """The blue team just scored a goal."""
    BALL_PLACEMENT_YELLOW: SSL_Referee.Command.ValueType  # 16
    """Equivalent to STOP, but the yellow team must pick up the ball and
    drop it in the Designated Position.
    """
    BALL_PLACEMENT_BLUE: SSL_Referee.Command.ValueType  # 17
    """Equivalent to STOP, but the blue team must pick up the ball and drop
    it in the Designated Position.
    """

    @typing_extensions.final
    class TeamInfo(google.protobuf.message.Message):
        """Information about a single team."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        SCORE_FIELD_NUMBER: builtins.int
        RED_CARDS_FIELD_NUMBER: builtins.int
        YELLOW_CARD_TIMES_FIELD_NUMBER: builtins.int
        YELLOW_CARDS_FIELD_NUMBER: builtins.int
        TIMEOUTS_FIELD_NUMBER: builtins.int
        TIMEOUT_TIME_FIELD_NUMBER: builtins.int
        GOALIE_FIELD_NUMBER: builtins.int
        FOUL_COUNTER_FIELD_NUMBER: builtins.int
        BALL_PLACEMENT_FAILURES_FIELD_NUMBER: builtins.int
        CAN_PLACE_BALL_FIELD_NUMBER: builtins.int
        MAX_ALLOWED_BOTS_FIELD_NUMBER: builtins.int
        BOT_SUBSTITUTION_INTENT_FIELD_NUMBER: builtins.int
        BALL_PLACEMENT_FAILURES_REACHED_FIELD_NUMBER: builtins.int
        name: builtins.str
        """The team's name (empty string if operator has not typed anything)."""
        score: builtins.int
        """The number of goals scored by the team during normal play and overtime."""
        red_cards: builtins.int
        """The number of red cards issued to the team since the beginning of the game."""
        @property
        def yellow_card_times(
            self,
        ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]:
            """The amount of time (in microseconds) left on each yellow card issued to the team.
            If no yellow cards are issued, this array has no elements.
            Otherwise, times are ordered from smallest to largest.
            """
        yellow_cards: builtins.int
        """The total number of yellow cards ever issued to the team."""
        timeouts: builtins.int
        """The number of timeouts this team can still call.
        If in a timeout right now, that timeout is excluded.
        """
        timeout_time: builtins.int
        """The number of microseconds of timeout this team can use."""
        goalie: builtins.int
        """The pattern number of this team's goalie."""
        foul_counter: builtins.int
        """The total number of countable fouls that act towards yellow cards"""
        ball_placement_failures: builtins.int
        """The number of consecutive ball placement failures of this team"""
        can_place_ball: builtins.bool
        """Indicate if the team is able and allowed to place the ball"""
        max_allowed_bots: builtins.int
        """The maximum number of bots allowed on the field based on division and cards"""
        bot_substitution_intent: builtins.bool
        """The team has submitted an intent to substitute one or more robots at the next chance"""
        ball_placement_failures_reached: builtins.bool
        """Indicate if the team reached the maximum allowed ball placement failures and is thus not allowed to place the ball anymore"""
        def __init__(
            self,
            *,
            name: builtins.str | None = ...,
            score: builtins.int | None = ...,
            red_cards: builtins.int | None = ...,
            yellow_card_times: collections.abc.Iterable[builtins.int] | None = ...,
            yellow_cards: builtins.int | None = ...,
            timeouts: builtins.int | None = ...,
            timeout_time: builtins.int | None = ...,
            goalie: builtins.int | None = ...,
            foul_counter: builtins.int | None = ...,
            ball_placement_failures: builtins.int | None = ...,
            can_place_ball: builtins.bool | None = ...,
            max_allowed_bots: builtins.int | None = ...,
            bot_substitution_intent: builtins.bool | None = ...,
            ball_placement_failures_reached: builtins.bool | None = ...,
        ) -> None: ...
        def HasField(
            self,
            field_name: typing_extensions.Literal[
                "ball_placement_failures",
                b"ball_placement_failures",
                "ball_placement_failures_reached",
                b"ball_placement_failures_reached",
                "bot_substitution_intent",
                b"bot_substitution_intent",
                "can_place_ball",
                b"can_place_ball",
                "foul_counter",
                b"foul_counter",
                "goalie",
                b"goalie",
                "max_allowed_bots",
                b"max_allowed_bots",
                "name",
                b"name",
                "red_cards",
                b"red_cards",
                "score",
                b"score",
                "timeout_time",
                b"timeout_time",
                "timeouts",
                b"timeouts",
                "yellow_cards",
                b"yellow_cards",
            ],
        ) -> builtins.bool: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal[
                "ball_placement_failures",
                b"ball_placement_failures",
                "ball_placement_failures_reached",
                b"ball_placement_failures_reached",
                "bot_substitution_intent",
                b"bot_substitution_intent",
                "can_place_ball",
                b"can_place_ball",
                "foul_counter",
                b"foul_counter",
                "goalie",
                b"goalie",
                "max_allowed_bots",
                b"max_allowed_bots",
                "name",
                b"name",
                "red_cards",
                b"red_cards",
                "score",
                b"score",
                "timeout_time",
                b"timeout_time",
                "timeouts",
                b"timeouts",
                "yellow_card_times",
                b"yellow_card_times",
                "yellow_cards",
                b"yellow_cards",
            ],
        ) -> None: ...

    @typing_extensions.final
    class Point(google.protobuf.message.Message):
        """The coordinates of the Designated Position. These are measured in
        millimetres and correspond to SSL-Vision coordinates. These fields are
        always either both present (in the case of a ball placement command) or
        both absent (in the case of any other command).
        """

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        X_FIELD_NUMBER: builtins.int
        Y_FIELD_NUMBER: builtins.int
        x: builtins.float
        y: builtins.float
        def __init__(
            self,
            *,
            x: builtins.float | None = ...,
            y: builtins.float | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["x", b"x", "y", b"y"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["x", b"x", "y", b"y"]) -> None: ...

    PACKET_TIMESTAMP_FIELD_NUMBER: builtins.int
    STAGE_FIELD_NUMBER: builtins.int
    STAGE_TIME_LEFT_FIELD_NUMBER: builtins.int
    COMMAND_FIELD_NUMBER: builtins.int
    COMMAND_COUNTER_FIELD_NUMBER: builtins.int
    COMMAND_TIMESTAMP_FIELD_NUMBER: builtins.int
    YELLOW_FIELD_NUMBER: builtins.int
    BLUE_FIELD_NUMBER: builtins.int
    DESIGNATED_POSITION_FIELD_NUMBER: builtins.int
    BLUETEAMONPOSITIVEHALF_FIELD_NUMBER: builtins.int
    GAMEEVENT_FIELD_NUMBER: builtins.int
    NEXT_COMMAND_FIELD_NUMBER: builtins.int
    GAME_EVENTS_OLD_FIELD_NUMBER: builtins.int
    GAME_EVENTS_FIELD_NUMBER: builtins.int
    PROPOSED_GAME_EVENTS_FIELD_NUMBER: builtins.int
    GAME_EVENT_PROPOSALS_FIELD_NUMBER: builtins.int
    SOURCE_IDENTIFIER_FIELD_NUMBER: builtins.int
    CURRENT_ACTION_TIME_REMAINING_FIELD_NUMBER: builtins.int
    packet_timestamp: builtins.int
    """The UNIX timestamp when the packet was sent, in microseconds.
    Divide by 1,000,000 to get a time_t.
    """
    stage: global___SSL_Referee.Stage.ValueType
    stage_time_left: builtins.int
    """The number of microseconds left in the stage.
    The following stages have this value; the rest do not:
    NORMAL_FIRST_HALF
    NORMAL_HALF_TIME
    NORMAL_SECOND_HALF
    EXTRA_TIME_BREAK
    EXTRA_FIRST_HALF
    EXTRA_HALF_TIME
    EXTRA_SECOND_HALF
    PENALTY_SHOOTOUT_BREAK

    If the stage runs over its specified time, this value
    becomes negative.
    """
    command: global___SSL_Referee.Command.ValueType
    command_counter: builtins.int
    """The number of commands issued since startup (mod 2^32)."""
    command_timestamp: builtins.int
    """The UNIX timestamp when the command was issued, in microseconds.
    This value changes only when a new command is issued, not on each packet.
    """
    @property
    def yellow(self) -> global___SSL_Referee.TeamInfo:
        """Information about the two teams."""
    @property
    def blue(self) -> global___SSL_Referee.TeamInfo: ...
    @property
    def designated_position(self) -> global___SSL_Referee.Point: ...
    blueTeamOnPositiveHalf: builtins.bool
    """Information about the direction of play.
    True, if the blue team will have it's goal on the positive x-axis of the ssl-vision coordinate system
    Obviously, the yellow team will play on the opposide half
    For compatibility, this field is optional
    """
    @property
    def gameEvent(self) -> ssl_referee_game_event_pb2.SSL_Referee_Game_Event:
        """The game event that caused the referee command"""
    next_command: global___SSL_Referee.Command.ValueType
    """The command that will be issued after the current stoppage and ball placement to continue the game."""
    @property
    def game_events_old(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        ssl_game_event_2019_pb2.GameEvent
    ]:
        """All game events that were detected since the last RUNNING state.
        Will be cleared as soon as the game is continued.
        """
    @property
    def game_events(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        ssl_game_event_2019_pb2.GameEvent
    ]: ...
    @property
    def proposed_game_events(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ProposedGameEvent]:
        """All non-finished proposed game events that may be processed next."""
    @property
    def game_event_proposals(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___GameEventProposalGroup
    ]: ...
    source_identifier: builtins.str
    """A random UUID of the source that is kept constant at the source while running
    If multiple sources are broadcasting to the same network, this id can be used to identify individual sources
    """
    current_action_time_remaining: builtins.int
    """The time in microseconds that is remaining until the current action times out
    The time will not be reset. It can get negative.
    An autoRef would raise an appropriate event, if the time gets negative.
    Possible actions where this time is relevant:
     * free kicks
     * kickoff, penalty kick, force start
     * ball placement
    """
    def __init__(
        self,
        *,
        packet_timestamp: builtins.int | None = ...,
        stage: global___SSL_Referee.Stage.ValueType | None = ...,
        stage_time_left: builtins.int | None = ...,
        command: global___SSL_Referee.Command.ValueType | None = ...,
        command_counter: builtins.int | None = ...,
        command_timestamp: builtins.int | None = ...,
        yellow: global___SSL_Referee.TeamInfo | None = ...,
        blue: global___SSL_Referee.TeamInfo | None = ...,
        designated_position: global___SSL_Referee.Point | None = ...,
        blueTeamOnPositiveHalf: builtins.bool | None = ...,
        gameEvent: ssl_referee_game_event_pb2.SSL_Referee_Game_Event | None = ...,
        next_command: global___SSL_Referee.Command.ValueType | None = ...,
        game_events_old: collections.abc.Iterable[ssl_game_event_2019_pb2.GameEvent] | None = ...,
        game_events: collections.abc.Iterable[ssl_game_event_2019_pb2.GameEvent] | None = ...,
        proposed_game_events: collections.abc.Iterable[global___ProposedGameEvent] | None = ...,
        game_event_proposals: collections.abc.Iterable[global___GameEventProposalGroup] | None = ...,
        source_identifier: builtins.str | None = ...,
        current_action_time_remaining: builtins.int | None = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "blue",
            b"blue",
            "blueTeamOnPositiveHalf",
            b"blueTeamOnPositiveHalf",
            "command",
            b"command",
            "command_counter",
            b"command_counter",
            "command_timestamp",
            b"command_timestamp",
            "current_action_time_remaining",
            b"current_action_time_remaining",
            "designated_position",
            b"designated_position",
            "gameEvent",
            b"gameEvent",
            "next_command",
            b"next_command",
            "packet_timestamp",
            b"packet_timestamp",
            "source_identifier",
            b"source_identifier",
            "stage",
            b"stage",
            "stage_time_left",
            b"stage_time_left",
            "yellow",
            b"yellow",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "blue",
            b"blue",
            "blueTeamOnPositiveHalf",
            b"blueTeamOnPositiveHalf",
            "command",
            b"command",
            "command_counter",
            b"command_counter",
            "command_timestamp",
            b"command_timestamp",
            "current_action_time_remaining",
            b"current_action_time_remaining",
            "designated_position",
            b"designated_position",
            "gameEvent",
            b"gameEvent",
            "game_event_proposals",
            b"game_event_proposals",
            "game_events",
            b"game_events",
            "game_events_old",
            b"game_events_old",
            "next_command",
            b"next_command",
            "packet_timestamp",
            b"packet_timestamp",
            "proposed_game_events",
            b"proposed_game_events",
            "source_identifier",
            b"source_identifier",
            "stage",
            b"stage",
            "stage_time_left",
            b"stage_time_left",
            "yellow",
            b"yellow",
        ],
    ) -> None: ...

global___SSL_Referee = SSL_Referee

@typing_extensions.final
class ProposedGameEvent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALID_UNTIL_FIELD_NUMBER: builtins.int
    PROPOSER_ID_FIELD_NUMBER: builtins.int
    GAME_EVENT_FIELD_NUMBER: builtins.int
    valid_until: builtins.int
    """The UNIX timestamp when the game event proposal will time out, in microseconds."""
    proposer_id: builtins.str
    """The identifier of the proposer."""
    @property
    def game_event(self) -> ssl_game_event_2019_pb2.GameEvent:
        """The proposed game event."""
    def __init__(
        self,
        *,
        valid_until: builtins.int | None = ...,
        proposer_id: builtins.str | None = ...,
        game_event: ssl_game_event_2019_pb2.GameEvent | None = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "game_event", b"game_event", "proposer_id", b"proposer_id", "valid_until", b"valid_until"
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "game_event", b"game_event", "proposer_id", b"proposer_id", "valid_until", b"valid_until"
        ],
    ) -> None: ...

global___ProposedGameEvent = ProposedGameEvent

@typing_extensions.final
class GameEventProposalGroup(google.protobuf.message.Message):
    """List of matching proposals"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GAME_EVENT_FIELD_NUMBER: builtins.int
    ACCEPTED_FIELD_NUMBER: builtins.int
    @property
    def game_event(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        ssl_game_event_2019_pb2.GameEvent
    ]:
        """The proposed game event."""
    accepted: builtins.bool
    """Whether the proposal group was accepted"""
    def __init__(
        self,
        *,
        game_event: collections.abc.Iterable[ssl_game_event_2019_pb2.GameEvent] | None = ...,
        accepted: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["accepted", b"accepted"]) -> builtins.bool: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["accepted", b"accepted", "game_event", b"game_event"]
    ) -> None: ...

global___GameEventProposalGroup = GameEventProposalGroup
