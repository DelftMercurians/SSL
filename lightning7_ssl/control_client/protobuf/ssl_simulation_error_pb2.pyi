"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class SimulatorError(google.protobuf.message.Message):
    """Errors in the simulator"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    code: builtins.str
    """Unique code of the error for automatic handling on client side"""
    message: builtins.str
    """Human readable description of the error"""
    def __init__(
        self,
        *,
        code: builtins.str | None = ...,
        message: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["code", b"code", "message", b"message"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["code", b"code", "message", b"message"]) -> None: ...

global___SimulatorError = SimulatorError