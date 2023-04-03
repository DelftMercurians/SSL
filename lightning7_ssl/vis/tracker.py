# A decorator for tracking changes to a class instance

from abc import ABC
from dataclasses import is_dataclass
from os import PathLike
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    TextIO,
    Tuple,
    Type,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

TypeMap = Dict[str, str]
JsonSerializable = Dict[str, "JsonSerializable"] | List["JsonSerializable"] | int | float | str | bool


def _to_snake_case(s: str) -> str:
    """Converts a string from PascalCase to snake_case."""
    result = ""
    for i, c in enumerate(s):
        if i > 0 and c.isupper():
            result += "_"
        result += c.lower()
    return result


def _to_dict(obj: object) -> Optional[JsonSerializable]:
    """Converts the object to a JSON-serializable dictionary.

    If an unsupported type is encountered, None is returned. If a field with an
    unsupported type is encountered, that field will be quietly ignored."""
    if isinstance(obj, TrackedBase) or (is_dataclass(obj) and not isinstance(obj, type)):
        field_names = get_type_hints(obj.__class__).keys()
        obj_dict = {}
        for k in field_names:
            v = getattr(obj, k)
            if k.startswith("_"):
                continue
            field_dict = _to_dict(v)
            if field_dict is None:
                continue
            obj_dict[_to_snake_case(k)] = field_dict
        return obj_dict
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            field_dict = _to_dict(v)
            if field_dict is None:
                continue
            new_dict[k] = field_dict
        return new_dict
    if isinstance(obj, (list, tuple, set)):
        new_list = []
        for v in obj:
            field_dict = _to_dict(v)
            if field_dict is None:
                continue
            new_list.append(field_dict)
        return new_list
    if obj is None or isinstance(obj, (int, float, str, bool)):
        return obj
    return None


def _get_ts_type(cls: Type, type_map: TypeMap) -> Optional[str]:
    """Gets the TypeScript type for the given class.

    If the class is a `TrackedBase` subclass or dataclass, it will be added to the
    type map and the type name will be returned (reference). Otherwise, the type will
    be inlined.

    If cls is an unsupported type, None will be returned. If cls contains a field
    with an unsupported type, that field will be quietly ignored.
    """
    if isinstance(cls, type):
        # TrackedBase and dataclasses
        if issubclass(cls, TrackedBase) or is_dataclass(cls):
            name = cls.__name__
            if name not in type_map:
                fields = get_type_hints(cls)
                docs = cls.__doc__
                lines = [(f"/** {docs.strip()} */" + "\n" if docs else "") + f"export interface {name} {{"]
                for k, v in fields.items():
                    if k.startswith("_"):
                        continue
                    ts_type = _get_ts_type(v, type_map)
                    if ts_type is None:
                        continue
                    lines.append(f"  {k}: {ts_type};")
                lines.append("}")
                type_map[name] = "\n".join(lines)
            return name
    # Collection types without type parameters
    if cls in (dict, Dict):
        return "Record<string, any>"
    if cls in (list, List, tuple, Tuple, set, Set):
        return "any[]"
    # Collection types with type parameters
    if get_origin(cls) in (dict, Dict):
        key, val = get_args(cls)
        if key not in (str, int):
            raise TypeError(f"Invalid key type for dict: {key}")
        value_type = _get_ts_type(val, type_map)
        return f"Record<string, {value_type}>" if value_type is not None else None
    if get_origin(cls) in (list, List, set, Set):
        element_type = _get_ts_type(get_args(cls)[0], type_map)
        return f"{element_type}[]" if element_type is not None else None
    if get_origin(cls) in (tuple, Tuple):
        # Handle ellipsis
        args = get_args(cls)
        if args[-1] is ...:
            element_type = _get_ts_type(args[0], type_map)
            return f"{element_type}[]" if element_type is not None else None
        # Handle fixed-length tuples
        element_types = [_get_ts_type(t, type_map) for t in args]
        if None in element_types:
            return None
        return f"[{', '.join(cast(List[str], element_types))}]"
    # Primitive types
    if cls in (int, float):
        return "number"
    if cls is str:
        return "string"
    if cls is bool:
        return "boolean"
    # Literal types
    if get_origin(cls) is Literal:
        args = get_args(cls)
        if any((not isinstance(a, (int, float, str, bool)) for a in args)):
            raise TypeError(f"Invalid literal type: {cls}")
        return " | ".join(((str(t).lower() if isinstance(t, bool) else repr(t)) for t in get_args(cls)))
    # Optional type
    if get_origin(cls) is Optional:
        opt_type = _get_ts_type(get_args(cls)[0], type_map)
        return f"{opt_type} | null" if opt_type is not None else None
    # None
    if cls is type(None):  # noqa: E721
        return "null"
    # Unknown, Any
    if cls in (object, type, Any):
        return "any"
    return None


class TrackedBase(ABC):
    """Base class for tracked objects.

    All subclasses of `TrackedBase` will be automatically tracked. Subclasses should
    define all fields as class attributes. For example:

    >>> class Foo(TrackedBase, root=True):
    ...     bar: int
    ...     baz: str

    Only fields defined as such will be included in the serialized output of `to_dict`
    and the generated TypeScript types.

    Calling `TrackableBase.to_dict` will return a dictionary representation of all
    tracked objects marked as `root`. For example:

    >>> foo = Foo(bar=1, baz="hello")
    >>> TrackedBase.to_dict()
    {'foo': {'bar': 1, 'baz': 'hello'}}

    Subclases that are not marked as `root` will only be included in the output of
    `to_dict` if they are referenced by a `root` subclass. For example:

    >>> class Foo(TrackedBase):
    ...     bar: int
    ...     baz: str
    >>> class Bar(TrackedBase, root=True):
    ...     foo: Foo
    >>> bar = Bar(foo=foo)
    >>> TrackedBase.to_dict()
    {'bar': {'foo': {'bar': 1, 'baz': 'hello'}}}

    Recursion also works for dataclasses:

    >>> @dataclass
    ... class Foo:
    ...     bar: int
    ...     baz: str
    >>> class Bar(TrackedBase, root=True):
    ...     foo: Foo
    >>> bar = Bar(foo=Foo(bar=1, baz="hello"))
    >>> TrackedBase.to_dict()
    {'bar': {'foo': {'bar': 1, 'baz': 'hello'}}}

    And for common collection types. If an unsupported type is encountered, it will be
    ignored and not included in the output of `to_dict`:

    >>> class Foo(TrackedBase, root=True):
    ...     bar: int
    ...     baz: List[str]
    ...     qux: List[UnspoortedType]
    >>> foo = Foo(bar=1, baz=["hello", "world"])
    >>> foo.qux = [UnspoortedType()]
    >>> TrackedBase.to_dict()
    {'foo': {'bar': 1, 'baz': ['hello', 'world']}}

    The `generate_types` method can be used to generate TypeScript types for all
    tracked objects. It will include an interface `State` whose type should match
    the return type of `to_dict`:

    >>> print(TrackedBase.generate_types())
    interface State {
        foo: Foo;
    }
    interface Foo {
        bar: number;
        baz: string;
    }

    The `write_types` method can be used to write the generated TypeScript types to a
    file.
    """

    def __init_subclass__(cls, /, root: bool = False, **kwargs) -> None:
        if not hasattr(TrackedBase, "__ts_types"):
            TrackedBase.__tracked_types = set()  # type: ignore
        if not hasattr(TrackedBase, "__tracked_instances"):
            TrackedBase.__tracked_instances = set()  # type: ignore
        if root:
            if issubclass(cls, TrackedBase) and cls is not TrackedBase:
                TrackedBase.__tracked_types.add(cls)  # type: ignore
                cls.__root = True  # type: ignore
        super().__init_subclass__(**kwargs)

    def __new__(cls):
        # We override __new__ instead of __init__ so that we can add the instance to
        # the tracked instances even if the subclass does not call super().__init__.
        instance = super().__new__(cls)
        if hasattr(cls, "__root") and cls.__root:  # type: ignore
            TrackedBase.__tracked_instances.add(instance)  # type: ignore
        return instance

    @staticmethod
    def to_dict() -> Dict:
        """Serializes all instances of `TrackedBase` marked as root to a dictionary.

        The dictionary has type:
        ```
        {
            [subclass_name]: {
                [field_name]: value
            }
        }
        ```

        Use `generate_ts_types` to generate TypeScript types for the return value.

        Returns:
            The dictionary."""
        return {
            _to_snake_case(obj.__class__.__name__): _to_dict(obj)
            for obj in TrackedBase.__tracked_instances  # type: ignore
            if isinstance(obj, TrackedBase)
        }

    @staticmethod
    def generate_ts_types() -> str:
        """Generates TypeScript types for the return value of `to_dict`.

        Only supports json-serializable types, including `TrackedBase` subclasses,
        dataclasses, collections, primitives, and literals.

        Fields starting with an underscore are ignored.

        Returns:
            The TypeScript types as a string."""
        types: TypeMap = {}
        state_type = (
            "export interface State {"
            + "\n".join(
                (
                    f"{_to_snake_case(cls.__name__)}: {_get_ts_type(cls, types)};"
                    for cls in TrackedBase.__tracked_types  # type: ignore
                )
            )
            + "\n}"
        )
        return "\n\n".join(types.values()) + "\n\n" + state_type

    @staticmethod
    def write_ts_types(file: PathLike | TextIO | str) -> None:
        """Writes TypeScript types to the given file.

        See `generate_ts_types` for supported types.

        Args:
            file: The file to write to. Can be a path, file object, or string."""
        type_str = TrackedBase.generate_ts_types()
        if isinstance(file, (str, PathLike)):
            with open(file, "w") as f:
                f.write(type_str)
        else:
            file.write(type_str)
