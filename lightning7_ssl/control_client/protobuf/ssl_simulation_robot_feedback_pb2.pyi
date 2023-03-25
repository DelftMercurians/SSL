"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.any_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import ssl_simulation_error_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class RobotFeedback(google.protobuf.message.Message):
    """Feedback from a robot"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    DRIBBLER_BALL_CONTACT_FIELD_NUMBER: builtins.int
    CUSTOM_FIELD_NUMBER: builtins.int
    id: builtins.int
    """Id of the robot"""
    dribbler_ball_contact: builtins.bool
    """Has the dribbler contact to the ball right now"""
    @property
    def custom(self) -> google.protobuf.any_pb2.Any:
        """Custom robot feedback for specific simulators (the protobuf files are managed by the simulators)"""
    def __init__(
        self,
        *,
        id: builtins.int | None = ...,
        dribbler_ball_contact: builtins.bool | None = ...,
        custom: google.protobuf.any_pb2.Any | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["custom", b"custom", "dribbler_ball_contact", b"dribbler_ball_contact", "id", b"id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["custom", b"custom", "dribbler_ball_contact", b"dribbler_ball_contact", "id", b"id"]) -> None: ...

global___RobotFeedback = RobotFeedback

@typing_extensions.final
class RobotControlResponse(google.protobuf.message.Message):
    """Response to RobotControl from the simulator to the connected client"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ERRORS_FIELD_NUMBER: builtins.int
    FEEDBACK_FIELD_NUMBER: builtins.int
    @property
    def errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[ssl_simulation_error_pb2.SimulatorError]:
        """List of errors, like using unsupported features"""
    @property
    def feedback(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RobotFeedback]:
        """Feedback of the robots"""
    def __init__(
        self,
        *,
        errors: collections.abc.Iterable[ssl_simulation_error_pb2.SimulatorError] | None = ...,
        feedback: collections.abc.Iterable[global___RobotFeedback] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["errors", b"errors", "feedback", b"feedback"]) -> None: ...

global___RobotControlResponse = RobotControlResponse