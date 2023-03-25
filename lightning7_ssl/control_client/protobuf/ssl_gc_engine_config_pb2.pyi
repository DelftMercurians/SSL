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
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Config(google.protobuf.message.Message):
    """The engine config"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Behavior:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _BehaviorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Config._Behavior.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        BEHAVIOR_UNKNOWN: Config._Behavior.ValueType  # 0
        """Not set or unknown"""
        BEHAVIOR_ACCEPT: Config._Behavior.ValueType  # 1
        """Always accept the game event"""
        BEHAVIOR_ACCEPT_MAJORITY: Config._Behavior.ValueType  # 2
        """Accept the game event if was reported by a majority"""
        BEHAVIOR_PROPOSE_ONLY: Config._Behavior.ValueType  # 3
        """Only propose the game event (can be accepted in the UI by a human)"""
        BEHAVIOR_LOG: Config._Behavior.ValueType  # 4
        """Only log the game event to the protocol"""
        BEHAVIOR_IGNORE: Config._Behavior.ValueType  # 5
        """Silently ignore the game event"""

    class Behavior(_Behavior, metaclass=_BehaviorEnumTypeWrapper):
        """Behaviors for each game event"""

    BEHAVIOR_UNKNOWN: Config.Behavior.ValueType  # 0
    """Not set or unknown"""
    BEHAVIOR_ACCEPT: Config.Behavior.ValueType  # 1
    """Always accept the game event"""
    BEHAVIOR_ACCEPT_MAJORITY: Config.Behavior.ValueType  # 2
    """Accept the game event if was reported by a majority"""
    BEHAVIOR_PROPOSE_ONLY: Config.Behavior.ValueType  # 3
    """Only propose the game event (can be accepted in the UI by a human)"""
    BEHAVIOR_LOG: Config.Behavior.ValueType  # 4
    """Only log the game event to the protocol"""
    BEHAVIOR_IGNORE: Config.Behavior.ValueType  # 5
    """Silently ignore the game event"""

    @typing_extensions.final
    class GameEventBehaviorEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: global___Config.Behavior.ValueType
        def __init__(
            self,
            *,
            key: builtins.str | None = ...,
            value: global___Config.Behavior.ValueType | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing_extensions.final
    class AutoRefConfigsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___AutoRefConfig: ...
        def __init__(
            self,
            *,
            key: builtins.str | None = ...,
            value: global___AutoRefConfig | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    GAME_EVENT_BEHAVIOR_FIELD_NUMBER: builtins.int
    AUTO_REF_CONFIGS_FIELD_NUMBER: builtins.int
    ACTIVE_TRACKER_SOURCE_FIELD_NUMBER: builtins.int
    TEAMS_FIELD_NUMBER: builtins.int
    @property
    def game_event_behavior(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, global___Config.Behavior.ValueType]:
        """The behavior for each game event"""
    @property
    def auto_ref_configs(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___AutoRefConfig]:
        """The config for each auto referee"""
    active_tracker_source: builtins.str
    """The selected tracker source"""
    @property
    def teams(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The list of available teams"""
    def __init__(
        self,
        *,
        game_event_behavior: collections.abc.Mapping[builtins.str, global___Config.Behavior.ValueType] | None = ...,
        auto_ref_configs: collections.abc.Mapping[builtins.str, global___AutoRefConfig] | None = ...,
        active_tracker_source: builtins.str | None = ...,
        teams: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["active_tracker_source", b"active_tracker_source"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["active_tracker_source", b"active_tracker_source", "auto_ref_configs", b"auto_ref_configs", "game_event_behavior", b"game_event_behavior", "teams", b"teams"]) -> None: ...

global___Config = Config

@typing_extensions.final
class AutoRefConfig(google.protobuf.message.Message):
    """The config for an auto referee"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Behavior:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _BehaviorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[AutoRefConfig._Behavior.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        BEHAVIOR_UNKNOWN: AutoRefConfig._Behavior.ValueType  # 0
        """Not set or unknown"""
        BEHAVIOR_ACCEPT: AutoRefConfig._Behavior.ValueType  # 1
        """Accept the game event"""
        BEHAVIOR_LOG: AutoRefConfig._Behavior.ValueType  # 2
        """Log the game event"""
        BEHAVIOR_IGNORE: AutoRefConfig._Behavior.ValueType  # 3
        """Silently ignore the game event"""

    class Behavior(_Behavior, metaclass=_BehaviorEnumTypeWrapper):
        """Behaviors for the game events reported by this auto referee"""

    BEHAVIOR_UNKNOWN: AutoRefConfig.Behavior.ValueType  # 0
    """Not set or unknown"""
    BEHAVIOR_ACCEPT: AutoRefConfig.Behavior.ValueType  # 1
    """Accept the game event"""
    BEHAVIOR_LOG: AutoRefConfig.Behavior.ValueType  # 2
    """Log the game event"""
    BEHAVIOR_IGNORE: AutoRefConfig.Behavior.ValueType  # 3
    """Silently ignore the game event"""

    @typing_extensions.final
    class GameEventBehaviorEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: global___AutoRefConfig.Behavior.ValueType
        def __init__(
            self,
            *,
            key: builtins.str | None = ...,
            value: global___AutoRefConfig.Behavior.ValueType | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    GAME_EVENT_BEHAVIOR_FIELD_NUMBER: builtins.int
    @property
    def game_event_behavior(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, global___AutoRefConfig.Behavior.ValueType]:
        """The game event behaviors for this auto referee"""
    def __init__(
        self,
        *,
        game_event_behavior: collections.abc.Mapping[builtins.str, global___AutoRefConfig.Behavior.ValueType] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["game_event_behavior", b"game_event_behavior"]) -> None: ...

global___AutoRefConfig = AutoRefConfig
