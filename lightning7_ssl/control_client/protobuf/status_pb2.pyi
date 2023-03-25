"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import debug_pb2
import gamestate_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import logfile_pb2
import robot_pb2
import sys
import typing
import userinput_pb2
import world_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class StrategyOption(google.protobuf.message.Message):
    """sent out by the strategy to tell that it offers this option"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DEFAULT_VALUE_FIELD_NUMBER: builtins.int
    name: builtins.str
    default_value: builtins.bool
    def __init__(
        self,
        *,
        name: builtins.str | None = ...,
        default_value: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["default_value", b"default_value", "name", b"name"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["default_value", b"default_value", "name", b"name"]) -> None: ...

global___StrategyOption = StrategyOption

@typing_extensions.final
class StatusStrategy(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _STATE:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _STATEEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[StatusStrategy._STATE.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        CLOSED: StatusStrategy._STATE.ValueType  # 1
        RUNNING: StatusStrategy._STATE.ValueType  # 3
        FAILED: StatusStrategy._STATE.ValueType  # 4
        COMPILING: StatusStrategy._STATE.ValueType  # 5

    class STATE(_STATE, metaclass=_STATEEnumTypeWrapper): ...
    CLOSED: StatusStrategy.STATE.ValueType  # 1
    RUNNING: StatusStrategy.STATE.ValueType  # 3
    FAILED: StatusStrategy.STATE.ValueType  # 4
    COMPILING: StatusStrategy.STATE.ValueType  # 5

    STATE_FIELD_NUMBER: builtins.int
    FILENAME_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    CURRENT_ENTRY_POINT_FIELD_NUMBER: builtins.int
    ENTRY_POINT_FIELD_NUMBER: builtins.int
    HAS_DEBUGGER_FIELD_NUMBER: builtins.int
    OPTIONS_FIELD_NUMBER: builtins.int
    state: global___StatusStrategy.STATE.ValueType
    filename: builtins.str
    name: builtins.str
    current_entry_point: builtins.str
    @property
    def entry_point(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    has_debugger: builtins.bool
    """deprecated = 6"""
    @property
    def options(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___StrategyOption]: ...
    def __init__(
        self,
        *,
        state: global___StatusStrategy.STATE.ValueType | None = ...,
        filename: builtins.str | None = ...,
        name: builtins.str | None = ...,
        current_entry_point: builtins.str | None = ...,
        entry_point: collections.abc.Iterable[builtins.str] | None = ...,
        has_debugger: builtins.bool | None = ...,
        options: collections.abc.Iterable[global___StrategyOption] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current_entry_point", b"current_entry_point", "filename", b"filename", "has_debugger", b"has_debugger", "name", b"name", "state", b"state"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["current_entry_point", b"current_entry_point", "entry_point", b"entry_point", "filename", b"filename", "has_debugger", b"has_debugger", "name", b"name", "options", b"options", "state", b"state"]) -> None: ...

global___StatusStrategy = StatusStrategy

@typing_extensions.final
class GitInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Kind:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _KindEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[GitInfo._Kind.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        BLUE: GitInfo._Kind.ValueType  # 1
        YELLOW: GitInfo._Kind.ValueType  # 2
        AUTOREF: GitInfo._Kind.ValueType  # 3
        RA: GitInfo._Kind.ValueType  # 4
        CONFIG: GitInfo._Kind.ValueType  # 5

    class Kind(_Kind, metaclass=_KindEnumTypeWrapper): ...
    BLUE: GitInfo.Kind.ValueType  # 1
    YELLOW: GitInfo.Kind.ValueType  # 2
    AUTOREF: GitInfo.Kind.ValueType  # 3
    RA: GitInfo.Kind.ValueType  # 4
    CONFIG: GitInfo.Kind.ValueType  # 5

    KIND_FIELD_NUMBER: builtins.int
    HASH_FIELD_NUMBER: builtins.int
    DIFF_FIELD_NUMBER: builtins.int
    MIN_HASH_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    kind: global___GitInfo.Kind.ValueType
    hash: builtins.str
    diff: builtins.str
    min_hash: builtins.str
    error: builtins.str
    def __init__(
        self,
        *,
        kind: global___GitInfo.Kind.ValueType | None = ...,
        hash: builtins.str | None = ...,
        diff: builtins.str | None = ...,
        min_hash: builtins.str | None = ...,
        error: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["diff", b"diff", "error", b"error", "hash", b"hash", "kind", b"kind", "min_hash", b"min_hash"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["diff", b"diff", "error", b"error", "hash", b"hash", "kind", b"kind", "min_hash", b"min_hash"]) -> None: ...

global___GitInfo = GitInfo

@typing_extensions.final
class StatusStrategyWrapper(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _StrategyType:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _StrategyTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[StatusStrategyWrapper._StrategyType.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        BLUE: StatusStrategyWrapper._StrategyType.ValueType  # 1
        YELLOW: StatusStrategyWrapper._StrategyType.ValueType  # 2
        AUTOREF: StatusStrategyWrapper._StrategyType.ValueType  # 3
        REPLAY_BLUE: StatusStrategyWrapper._StrategyType.ValueType  # 4
        REPLAY_YELLOW: StatusStrategyWrapper._StrategyType.ValueType  # 5

    class StrategyType(_StrategyType, metaclass=_StrategyTypeEnumTypeWrapper): ...
    BLUE: StatusStrategyWrapper.StrategyType.ValueType  # 1
    YELLOW: StatusStrategyWrapper.StrategyType.ValueType  # 2
    AUTOREF: StatusStrategyWrapper.StrategyType.ValueType  # 3
    REPLAY_BLUE: StatusStrategyWrapper.StrategyType.ValueType  # 4
    REPLAY_YELLOW: StatusStrategyWrapper.StrategyType.ValueType  # 5

    TYPE_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    type: global___StatusStrategyWrapper.StrategyType.ValueType
    @property
    def status(self) -> global___StatusStrategy: ...
    def __init__(
        self,
        *,
        type: global___StatusStrategyWrapper.StrategyType.ValueType | None = ...,
        status: global___StatusStrategy | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["status", b"status", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["status", b"status", "type", b"type"]) -> None: ...

global___StatusStrategyWrapper = StatusStrategyWrapper

@typing_extensions.final
class Timing(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BLUE_TOTAL_FIELD_NUMBER: builtins.int
    BLUE_PATH_FIELD_NUMBER: builtins.int
    YELLOW_TOTAL_FIELD_NUMBER: builtins.int
    YELLOW_PATH_FIELD_NUMBER: builtins.int
    AUTOREF_TOTAL_FIELD_NUMBER: builtins.int
    TRACKING_FIELD_NUMBER: builtins.int
    CONTROLLER_FIELD_NUMBER: builtins.int
    TRANSCEIVER_FIELD_NUMBER: builtins.int
    TRANSCEIVER_RTT_FIELD_NUMBER: builtins.int
    SIMULATOR_FIELD_NUMBER: builtins.int
    blue_total: builtins.float
    blue_path: builtins.float
    yellow_total: builtins.float
    yellow_path: builtins.float
    autoref_total: builtins.float
    tracking: builtins.float
    controller: builtins.float
    transceiver: builtins.float
    transceiver_rtt: builtins.float
    simulator: builtins.float
    def __init__(
        self,
        *,
        blue_total: builtins.float | None = ...,
        blue_path: builtins.float | None = ...,
        yellow_total: builtins.float | None = ...,
        yellow_path: builtins.float | None = ...,
        autoref_total: builtins.float | None = ...,
        tracking: builtins.float | None = ...,
        controller: builtins.float | None = ...,
        transceiver: builtins.float | None = ...,
        transceiver_rtt: builtins.float | None = ...,
        simulator: builtins.float | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["autoref_total", b"autoref_total", "blue_path", b"blue_path", "blue_total", b"blue_total", "controller", b"controller", "simulator", b"simulator", "tracking", b"tracking", "transceiver", b"transceiver", "transceiver_rtt", b"transceiver_rtt", "yellow_path", b"yellow_path", "yellow_total", b"yellow_total"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["autoref_total", b"autoref_total", "blue_path", b"blue_path", "blue_total", b"blue_total", "controller", b"controller", "simulator", b"simulator", "tracking", b"tracking", "transceiver", b"transceiver", "transceiver_rtt", b"transceiver_rtt", "yellow_path", b"yellow_path", "yellow_total", b"yellow_total"]) -> None: ...

global___Timing = Timing

@typing_extensions.final
class StatusTransceiver(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACTIVE_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    DROPPED_USB_PACKETS_FIELD_NUMBER: builtins.int
    DROPPED_COMMANDS_FIELD_NUMBER: builtins.int
    active: builtins.bool
    error: builtins.str
    dropped_usb_packets: builtins.int
    dropped_commands: builtins.int
    def __init__(
        self,
        *,
        active: builtins.bool | None = ...,
        error: builtins.str | None = ...,
        dropped_usb_packets: builtins.int | None = ...,
        dropped_commands: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["active", b"active", "dropped_commands", b"dropped_commands", "dropped_usb_packets", b"dropped_usb_packets", "error", b"error"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["active", b"active", "dropped_commands", b"dropped_commands", "dropped_usb_packets", b"dropped_usb_packets", "error", b"error"]) -> None: ...

global___StatusTransceiver = StatusTransceiver

@typing_extensions.final
class PortBindError(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PORT_FIELD_NUMBER: builtins.int
    port: builtins.int
    def __init__(
        self,
        *,
        port: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["port", b"port"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["port", b"port"]) -> None: ...

global___PortBindError = PortBindError

@typing_extensions.final
class OptionStatus(google.protobuf.message.Message):
    """tells the strategy and ui if an option is enabled or not"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    name: builtins.str
    value: builtins.bool
    def __init__(
        self,
        *,
        name: builtins.str | None = ...,
        value: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["name", b"name", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "value", b"value"]) -> None: ...

global___OptionStatus = OptionStatus

@typing_extensions.final
class StatusGameController(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _GameControllerState:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _GameControllerStateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[StatusGameController._GameControllerState.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        STOPPED: StatusGameController._GameControllerState.ValueType  # 1
        STARTING: StatusGameController._GameControllerState.ValueType  # 2
        RUNNING: StatusGameController._GameControllerState.ValueType  # 3
        CRASHED: StatusGameController._GameControllerState.ValueType  # 4
        NOT_RESPONDING: StatusGameController._GameControllerState.ValueType  # 5

    class GameControllerState(_GameControllerState, metaclass=_GameControllerStateEnumTypeWrapper): ...
    STOPPED: StatusGameController.GameControllerState.ValueType  # 1
    STARTING: StatusGameController.GameControllerState.ValueType  # 2
    RUNNING: StatusGameController.GameControllerState.ValueType  # 3
    CRASHED: StatusGameController.GameControllerState.ValueType  # 4
    NOT_RESPONDING: StatusGameController.GameControllerState.ValueType  # 5

    CURRENT_STATE_FIELD_NUMBER: builtins.int
    current_state: global___StatusGameController.GameControllerState.ValueType
    def __init__(
        self,
        *,
        current_state: global___StatusGameController.GameControllerState.ValueType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["current_state", b"current_state"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["current_state", b"current_state"]) -> None: ...

global___StatusGameController = StatusGameController

@typing_extensions.final
class StatusAmun(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PORT_BIND_ERROR_FIELD_NUMBER: builtins.int
    OPTIONS_FIELD_NUMBER: builtins.int
    GAME_CONTROLLER_FIELD_NUMBER: builtins.int
    @property
    def port_bind_error(self) -> global___PortBindError: ...
    @property
    def options(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OptionStatus]: ...
    @property
    def game_controller(self) -> global___StatusGameController: ...
    def __init__(
        self,
        *,
        port_bind_error: global___PortBindError | None = ...,
        options: collections.abc.Iterable[global___OptionStatus] | None = ...,
        game_controller: global___StatusGameController | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["game_controller", b"game_controller", "port_bind_error", b"port_bind_error"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["game_controller", b"game_controller", "options", b"options", "port_bind_error", b"port_bind_error"]) -> None: ...

global___StatusAmun = StatusAmun

@typing_extensions.final
class Status(google.protobuf.message.Message):
    """The status message is dumped for log replay
    -> take care not to break compatibility!
    WARNING: every message containing timestamps must be rewritten in the logcutter
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIME_FIELD_NUMBER: builtins.int
    GAME_STATE_FIELD_NUMBER: builtins.int
    WORLD_STATE_FIELD_NUMBER: builtins.int
    GEOMETRY_FIELD_NUMBER: builtins.int
    TEAM_BLUE_FIELD_NUMBER: builtins.int
    TEAM_YELLOW_FIELD_NUMBER: builtins.int
    STRATEGY_BLUE_FIELD_NUMBER: builtins.int
    STRATEGY_YELLOW_FIELD_NUMBER: builtins.int
    STRATEGY_AUTOREF_FIELD_NUMBER: builtins.int
    DEBUG_FIELD_NUMBER: builtins.int
    TIMING_FIELD_NUMBER: builtins.int
    RADIO_COMMAND_FIELD_NUMBER: builtins.int
    TRANSCEIVER_FIELD_NUMBER: builtins.int
    USER_INPUT_BLUE_FIELD_NUMBER: builtins.int
    USER_INPUT_YELLOW_FIELD_NUMBER: builtins.int
    AMUN_STATE_FIELD_NUMBER: builtins.int
    TIMER_SCALING_FIELD_NUMBER: builtins.int
    BLUE_RUNNING_FIELD_NUMBER: builtins.int
    YELLOW_RUNNING_FIELD_NUMBER: builtins.int
    AUTOREF_RUNNING_FIELD_NUMBER: builtins.int
    EXECUTION_STATE_FIELD_NUMBER: builtins.int
    EXECUTION_GAME_STATE_FIELD_NUMBER: builtins.int
    EXECUTION_USER_INPUT_FIELD_NUMBER: builtins.int
    LOG_ID_FIELD_NUMBER: builtins.int
    ORIGINAL_FRAME_NUMBER_FIELD_NUMBER: builtins.int
    STATUS_STRATEGY_FIELD_NUMBER: builtins.int
    PURE_UI_RESPONSE_FIELD_NUMBER: builtins.int
    GIT_INFO_FIELD_NUMBER: builtins.int
    time: builtins.int
    @property
    def game_state(self) -> gamestate_pb2.GameState:
        """optional deprecated.amun.GameState game_state_deprecated = 2;"""
    @property
    def world_state(self) -> world_pb2.State: ...
    @property
    def geometry(self) -> world_pb2.Geometry: ...
    @property
    def team_blue(self) -> robot_pb2.Team: ...
    @property
    def team_yellow(self) -> robot_pb2.Team: ...
    @property
    def strategy_blue(self) -> global___StatusStrategy:
        """deprecated"""
    @property
    def strategy_yellow(self) -> global___StatusStrategy:
        """deprecated"""
    @property
    def strategy_autoref(self) -> global___StatusStrategy:
        """deprecated"""
    @property
    def debug(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[debug_pb2.DebugValues]: ...
    @property
    def timing(self) -> global___Timing: ...
    @property
    def radio_command(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[robot_pb2.RadioCommand]: ...
    @property
    def transceiver(self) -> global___StatusTransceiver: ...
    @property
    def user_input_blue(self) -> userinput_pb2.UserInput:
        """deprecated = 14;"""
    @property
    def user_input_yellow(self) -> userinput_pb2.UserInput: ...
    @property
    def amun_state(self) -> global___StatusAmun: ...
    timer_scaling: builtins.float
    blue_running: builtins.bool
    yellow_running: builtins.bool
    autoref_running: builtins.bool
    @property
    def execution_state(self) -> world_pb2.State: ...
    @property
    def execution_game_state(self) -> gamestate_pb2.GameState: ...
    @property
    def execution_user_input(self) -> userinput_pb2.UserInput: ...
    @property
    def log_id(self) -> logfile_pb2.Uid: ...
    original_frame_number: builtins.int
    @property
    def status_strategy(self) -> global___StatusStrategyWrapper: ...
    @property
    def pure_ui_response(self) -> global___UiResponse:
        """NOTE: ANY STATUS containing this message will not be serialized in a log."""
    @property
    def git_info(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GitInfo]: ...
    def __init__(
        self,
        *,
        time: builtins.int | None = ...,
        game_state: gamestate_pb2.GameState | None = ...,
        world_state: world_pb2.State | None = ...,
        geometry: world_pb2.Geometry | None = ...,
        team_blue: robot_pb2.Team | None = ...,
        team_yellow: robot_pb2.Team | None = ...,
        strategy_blue: global___StatusStrategy | None = ...,
        strategy_yellow: global___StatusStrategy | None = ...,
        strategy_autoref: global___StatusStrategy | None = ...,
        debug: collections.abc.Iterable[debug_pb2.DebugValues] | None = ...,
        timing: global___Timing | None = ...,
        radio_command: collections.abc.Iterable[robot_pb2.RadioCommand] | None = ...,
        transceiver: global___StatusTransceiver | None = ...,
        user_input_blue: userinput_pb2.UserInput | None = ...,
        user_input_yellow: userinput_pb2.UserInput | None = ...,
        amun_state: global___StatusAmun | None = ...,
        timer_scaling: builtins.float | None = ...,
        blue_running: builtins.bool | None = ...,
        yellow_running: builtins.bool | None = ...,
        autoref_running: builtins.bool | None = ...,
        execution_state: world_pb2.State | None = ...,
        execution_game_state: gamestate_pb2.GameState | None = ...,
        execution_user_input: userinput_pb2.UserInput | None = ...,
        log_id: logfile_pb2.Uid | None = ...,
        original_frame_number: builtins.int | None = ...,
        status_strategy: global___StatusStrategyWrapper | None = ...,
        pure_ui_response: global___UiResponse | None = ...,
        git_info: collections.abc.Iterable[global___GitInfo] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["amun_state", b"amun_state", "autoref_running", b"autoref_running", "blue_running", b"blue_running", "execution_game_state", b"execution_game_state", "execution_state", b"execution_state", "execution_user_input", b"execution_user_input", "game_state", b"game_state", "geometry", b"geometry", "log_id", b"log_id", "original_frame_number", b"original_frame_number", "pure_ui_response", b"pure_ui_response", "status_strategy", b"status_strategy", "strategy_autoref", b"strategy_autoref", "strategy_blue", b"strategy_blue", "strategy_yellow", b"strategy_yellow", "team_blue", b"team_blue", "team_yellow", b"team_yellow", "time", b"time", "timer_scaling", b"timer_scaling", "timing", b"timing", "transceiver", b"transceiver", "user_input_blue", b"user_input_blue", "user_input_yellow", b"user_input_yellow", "world_state", b"world_state", "yellow_running", b"yellow_running"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["amun_state", b"amun_state", "autoref_running", b"autoref_running", "blue_running", b"blue_running", "debug", b"debug", "execution_game_state", b"execution_game_state", "execution_state", b"execution_state", "execution_user_input", b"execution_user_input", "game_state", b"game_state", "geometry", b"geometry", "git_info", b"git_info", "log_id", b"log_id", "original_frame_number", b"original_frame_number", "pure_ui_response", b"pure_ui_response", "radio_command", b"radio_command", "status_strategy", b"status_strategy", "strategy_autoref", b"strategy_autoref", "strategy_blue", b"strategy_blue", "strategy_yellow", b"strategy_yellow", "team_blue", b"team_blue", "team_yellow", b"team_yellow", "time", b"time", "timer_scaling", b"timer_scaling", "timing", b"timing", "transceiver", b"transceiver", "user_input_blue", b"user_input_blue", "user_input_yellow", b"user_input_yellow", "world_state", b"world_state", "yellow_running", b"yellow_running"]) -> None: ...

global___Status = Status

@typing_extensions.final
class UiResponse(google.protobuf.message.Message):
    """This message can be used for pure user-ui-response.
    It will be cut out when writing to log, therefore modifications
    can be done without breaking log compatibility.
    DO NOT use this message for information that could be useful in a logfile!
    DO NOT add a UIResponse to a normal Status, send a NEW STATUS instead.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENABLE_LOGGING_FIELD_NUMBER: builtins.int
    LOGGING_INFO_FIELD_NUMBER: builtins.int
    LOGGER_STATUS_FIELD_NUMBER: builtins.int
    PLAYBACK_BURST_END_FIELD_NUMBER: builtins.int
    PLAYBACK_PAUSED_FIELD_NUMBER: builtins.int
    LOG_INFO_FIELD_NUMBER: builtins.int
    FRAME_NUMBER_FIELD_NUMBER: builtins.int
    FORCE_RA_HORUS_FIELD_NUMBER: builtins.int
    LOG_OPEN_FIELD_NUMBER: builtins.int
    EXPORT_VISIONLOG_ERROR_FIELD_NUMBER: builtins.int
    REQUESTED_LOG_UID_FIELD_NUMBER: builtins.int
    LOG_OFFERS_FIELD_NUMBER: builtins.int
    LOG_UID_PARSER_ERROR_FIELD_NUMBER: builtins.int
    enable_logging: builtins.bool
    @property
    def logging_info(self) -> global___LoggingInfo: ...
    @property
    def logger_status(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Status]:
        """used for the plotter right now"""
    playback_burst_end: builtins.bool
    """used to notify logslider to update its position to Status::time"""
    playback_paused: builtins.bool
    @property
    def log_info(self) -> global___LogPlaybackInfo: ...
    frame_number: builtins.int
    force_ra_horus: builtins.bool
    """true if forced Ra, false if forced Horus"""
    @property
    def log_open(self) -> global___LogfileOpenInfo: ...
    export_visionlog_error: builtins.str
    requested_log_uid: builtins.str
    @property
    def log_offers(self) -> logfile_pb2.LogOffer: ...
    log_uid_parser_error: builtins.str
    def __init__(
        self,
        *,
        enable_logging: builtins.bool | None = ...,
        logging_info: global___LoggingInfo | None = ...,
        logger_status: collections.abc.Iterable[global___Status] | None = ...,
        playback_burst_end: builtins.bool | None = ...,
        playback_paused: builtins.bool | None = ...,
        log_info: global___LogPlaybackInfo | None = ...,
        frame_number: builtins.int | None = ...,
        force_ra_horus: builtins.bool | None = ...,
        log_open: global___LogfileOpenInfo | None = ...,
        export_visionlog_error: builtins.str | None = ...,
        requested_log_uid: builtins.str | None = ...,
        log_offers: logfile_pb2.LogOffer | None = ...,
        log_uid_parser_error: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["enable_logging", b"enable_logging", "export_visionlog_error", b"export_visionlog_error", "force_ra_horus", b"force_ra_horus", "frame_number", b"frame_number", "log_info", b"log_info", "log_offers", b"log_offers", "log_open", b"log_open", "log_uid_parser_error", b"log_uid_parser_error", "logging_info", b"logging_info", "playback_burst_end", b"playback_burst_end", "playback_paused", b"playback_paused", "requested_log_uid", b"requested_log_uid"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["enable_logging", b"enable_logging", "export_visionlog_error", b"export_visionlog_error", "force_ra_horus", b"force_ra_horus", "frame_number", b"frame_number", "log_info", b"log_info", "log_offers", b"log_offers", "log_open", b"log_open", "log_uid_parser_error", b"log_uid_parser_error", "logger_status", b"logger_status", "logging_info", b"logging_info", "playback_burst_end", b"playback_burst_end", "playback_paused", b"playback_paused", "requested_log_uid", b"requested_log_uid"]) -> None: ...

global___UiResponse = UiResponse

@typing_extensions.final
class LoggingInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IS_LOGGING_FIELD_NUMBER: builtins.int
    IS_REPLAY_LOGGER_FIELD_NUMBER: builtins.int
    is_logging: builtins.bool
    is_replay_logger: builtins.bool
    def __init__(
        self,
        *,
        is_logging: builtins.bool | None = ...,
        is_replay_logger: builtins.bool | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["is_logging", b"is_logging", "is_replay_logger", b"is_replay_logger"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["is_logging", b"is_logging", "is_replay_logger", b"is_replay_logger"]) -> None: ...

global___LoggingInfo = LoggingInfo

@typing_extensions.final
class LogPlaybackInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    START_TIME_FIELD_NUMBER: builtins.int
    DURATION_FIELD_NUMBER: builtins.int
    PACKET_COUNT_FIELD_NUMBER: builtins.int
    start_time: builtins.int
    duration: builtins.int
    packet_count: builtins.int
    def __init__(
        self,
        *,
        start_time: builtins.int | None = ...,
        duration: builtins.int | None = ...,
        packet_count: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["duration", b"duration", "packet_count", b"packet_count", "start_time", b"start_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["duration", b"duration", "packet_count", b"packet_count", "start_time", b"start_time"]) -> None: ...

global___LogPlaybackInfo = LogPlaybackInfo

@typing_extensions.final
class LogfileOpenInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SUCCESS_FIELD_NUMBER: builtins.int
    FILENAME_FIELD_NUMBER: builtins.int
    success: builtins.bool
    filename: builtins.str
    """filename if success = true, error-message if success = false"""
    def __init__(
        self,
        *,
        success: builtins.bool | None = ...,
        filename: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["filename", b"filename", "success", b"success"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["filename", b"filename", "success", b"success"]) -> None: ...

global___LogfileOpenInfo = LogfileOpenInfo