"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Protocol to communicate rough plans to other teammates
Units are specified as follows:
length - millimeters
time - seconds
angle - radians
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
class TeamPlan(google.protobuf.message.Message):
    """Plan of a list of robots"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PLANS_FIELD_NUMBER: builtins.int
    @property
    def plans(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RobotPlan]: ...
    def __init__(
        self,
        *,
        plans: collections.abc.Iterable[global___RobotPlan] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["plans", b"plans"]) -> None: ...

global___TeamPlan = TeamPlan

@typing_extensions.final
class RobotPlan(google.protobuf.message.Message):
    """Plan of a single robot"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _RobotRole:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _RobotRoleEnumTypeWrapper(
        google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[RobotPlan._RobotRole.ValueType],
        builtins.type,
    ):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        Default: RobotPlan._RobotRole.ValueType  # 0
        """no specified role"""
        Goalie: RobotPlan._RobotRole.ValueType  # 1
        Defense: RobotPlan._RobotRole.ValueType  # 2
        Offense: RobotPlan._RobotRole.ValueType  # 3

    class RobotRole(_RobotRole, metaclass=_RobotRoleEnumTypeWrapper):
        """Different roles a robot can assume"""

    Default: RobotPlan.RobotRole.ValueType  # 0
    """no specified role"""
    Goalie: RobotPlan.RobotRole.ValueType  # 1
    Defense: RobotPlan.RobotRole.ValueType  # 2
    Offense: RobotPlan.RobotRole.ValueType  # 3

    ROBOT_ID_FIELD_NUMBER: builtins.int
    ROLE_FIELD_NUMBER: builtins.int
    NAV_TARGET_FIELD_NUMBER: builtins.int
    SHOT_TARGET_FIELD_NUMBER: builtins.int
    robot_id: builtins.int
    """ID of the robot from SSL vision"""
    role: global___RobotPlan.RobotRole.ValueType
    """Planned role of this robot"""
    @property
    def nav_target(self) -> global___Pose:
        """Planned navigation target"""
    @property
    def shot_target(self) -> global___Location:
        """Planned shot target"""
    def __init__(
        self,
        *,
        robot_id: builtins.int | None = ...,
        role: global___RobotPlan.RobotRole.ValueType | None = ...,
        nav_target: global___Pose | None = ...,
        shot_target: global___Location | None = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "nav_target",
            b"nav_target",
            "robot_id",
            b"robot_id",
            "role",
            b"role",
            "shot_target",
            b"shot_target",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "nav_target",
            b"nav_target",
            "robot_id",
            b"robot_id",
            "role",
            b"role",
            "shot_target",
            b"shot_target",
        ],
    ) -> None: ...

global___RobotPlan = RobotPlan

@typing_extensions.final
class Location(google.protobuf.message.Message):
    """Location message, in mm. The center of the field is specified as (0, 0).
    Positive x axis points to the opponent's goal
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    x: builtins.int
    y: builtins.int
    def __init__(
        self,
        *,
        x: builtins.int | None = ...,
        y: builtins.int | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["x", b"x", "y", b"y"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["x", b"x", "y", b"y"]) -> None: ...

global___Location = Location

@typing_extensions.final
class Pose(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LOC_FIELD_NUMBER: builtins.int
    HEADING_FIELD_NUMBER: builtins.int
    @property
    def loc(self) -> global___Location:
        """location of the robot"""
    heading: builtins.float
    """heading of the robot"""
    def __init__(
        self,
        *,
        loc: global___Location | None = ...,
        heading: builtins.float | None = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["heading", b"heading", "loc", b"loc"]
    ) -> builtins.bool: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["heading", b"heading", "loc", b"loc"]
    ) -> None: ...

global___Pose = Pose
