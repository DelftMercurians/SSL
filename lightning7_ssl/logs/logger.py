import inspect
import json
import sys
import time
from collections.abc import Iterable
from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Optional


def to_json_serializable(obj):
    """Converts an object to a JSON serializable object."""
    if is_dataclass(obj):
        return asdict(obj)
    elif inspect.isclass(obj):
        try:
            return obj.to_json()  # type: ignore
        except AttributeError:
            return {
                k: to_json_serializable(getattr(obj, k, None))
                for k in obj.__annotations__.keys()
                if not k.startswith("_")
            }
    elif isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, Iterable) and not isinstance(obj, str):
        return [to_json_serializable(v) for v in obj]
    else:
        return obj


class Logger:
    def __init__(self):
        self.backends = []
        self.filters = []
        self.tracked_objects = []

    def add_backend(self, backend):
        self.backends.append(backend)

    def add_filter(self, filter_func: Callable):
        self.filters.append(filter_func)

    def add_tracked(self, tracked_object):
        self.tracked_objects.append(tracked_object)

    def log(self, log_level: str, value: Any, *, tag: Optional[str] = None, obj: Optional[Any] = None):
        value = to_json_serializable(value)
        log_obj = {"level": log_level, "value": value, "time": time.time()}

        if isinstance(tag, str):
            log_obj["tag"] = tag
        if obj is not None:
            obj_tag = str(type(obj).__name__)
            if hasattr(obj, "id"):
                id_ = getattr(obj, "id")
                if callable(id_):
                    id_ = id_()
                obj_tag += f".{id_}"
            log_obj["object"] = obj_tag

        if not all(filter_func(log_obj) for filter_func in self.filters):
            return

        json_str = None
        for backend in self.backends:
            if hasattr(backend, "log_json"):
                backend.log_json(log_obj)
            elif hasattr(backend, "log_str"):
                if json_str is None:
                    json_str = json.dumps(log_obj)
                backend.log_str(json_str)

    def log_tracked(self):
        for obj in self.tracked_objects:
            self.log("info", obj, obj=obj)


class StdoutBackend:
    def log_str(self, log_obj_str):
        sys.stdout.write(log_obj_str + "\n")


class FileBackend:
    def __init__(self, file_path):
        self.file_path = file_path

    def log_str(self, log_obj_str):
        with open(self.file_path, "a") as f:
            f.write(log_obj_str + "\n")
