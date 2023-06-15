from typing import Any, Optional

from .logger import Logger

_logger: Logger | None = None


def setup_logger(backends, filters=[]):
    global _logger
    if _logger is not None:
        raise RuntimeError("Logger already initialized")
    _logger = Logger()
    for backend in backends:
        assert hasattr(backend, "log_str") or hasattr(backend, "log_json")
        _logger.add_backend(backend)

    for filter_func in filters:
        assert callable(filter_func)
        _logger.add_filter(filter_func)


def log(value, tag: Optional[str] = None, obj: Optional[Any] = None):
    if _logger is not None:
        _logger.log("info", value, tag=tag, obj=obj)


def log_warn(value, tag: Optional[str] = None, obj: Optional[Any] = None):
    if _logger is not None:
        _logger.log("warn", value, tag=tag, obj=obj)


def log_err(value, tag: Optional[str] = None, obj: Optional[Any] = None):
    if _logger is not None:
        _logger.log("err", value, tag=tag, obj=obj)


def log_tracked():
    if _logger is not None:
        _logger.log_tracked()


class Tracked:
    def __new__(cls) -> "Tracked":
        obj = super().__new__(cls)
        if _logger is not None:
            _logger.add_tracked(obj)
        return obj


__all__ = ["setup_logger", "log", "log_warn", "log_err", "log_tracked", "Tracked"]
