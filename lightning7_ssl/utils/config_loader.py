import argparse
import os
import tomllib
from typing import Literal, get_args, get_origin, get_type_hints


def try_load_from_env_var(value: str, type_):
    """Try to load a value from an environment variable."""
    if type_ is bool:
        return value.lower() in ("true", "1")
    elif type_ is int:
        return int(value)
    elif type_ is float:
        return float(value)
    elif type_ is str:
        return value
    elif get_origin(type_) is Literal:
        variants = get_args(type_)
        if value in variants:
            return value
        else:
            raise ValueError(f"Invalid value: {value}")
    else:
        raise TypeError(f"Unsupported type: {type_}")


def try_parse_docstring(docstring: str | None, fields: list[str]) -> dict[str, str]:
    if docstring is None:
        return {}
    docstring = docstring.strip()
    if docstring.startswith("'''") and docstring.endswith("'''"):
        docstring = docstring[3:-3]
    elif docstring.startswith('"""') and docstring.endswith('"""'):
        docstring = docstring[3:-3]
    else:
        return {}
    docstring = docstring.strip()
    if docstring == "":
        return {}
    # Find "Attributes:" section
    attributes_section: list[str] | None = None
    for line in docstring.splitlines():
        line = line.strip()
        if line.startswith("Attributes:"):
            attributes_section = []
        elif attributes_section is not None:
            if line and line != "":
                attributes_section.append(line)
            else:
                break
    if attributes_section is None or len(attributes_section) == 0:
        return {}
    # Parse attributes
    result: dict[str, str] = {}
    for line in attributes_section:
        if line.startswith("- "):
            line = line[2:]
        if line.startswith("* "):
            line = line[2:]
        line = line.strip()
        if ": " in line:
            var_name, var_help = line.split(": ", 1)
            var_name = var_name.strip()
            var_help = var_help.strip()
            if var_name in fields:
                result[var_name] = var_help
            else:
                continue
        else:
            continue
    return result


class ConfigLoader:
    """Loads configuration variables from (in order of precedence):
    1. Override dictionary (kwargs passed to the constructor)
    2. Command line arguments (`--snake-case`)
    3. Environment variables (`SNAKE_CASE`)
    4. TOML file (`snake_case`), defaults to `config.toml`
    5. Defaults specified in the class definition

    Subclasses should define configuration variables as class attributes with
    type annotations and optional default values.

    Currently supported types (for all methods) are: `bool`, `int`, `float`, `str`, and
    `Literal[...]`. New types should be added on demand.

    Usage example:
    >>> class Config(ConfigLoader):
    ...     foo: int = 1
    ...     bar: str = "baz"
    ...     baz: bool
    >>> config = Config(config_file="config.toml") # optionally specify config file
    >>> config.foo
    1

    Configuration variables must be all lowercase and must not start with an underscore.

    To provide a help message for a configuration variable, add a docstring to the subclass
    with the following format:
    >>> class Config(ConfigLoader):
    ...     '''This is the help message for the config class.
    ...
    ...     Attributes:
    ...         foo: This is the help message for the foo variable.
    ...     '''
    ...
    ...     foo: int = 1
    """

    def __init__(
        self,
        *,
        parser_prog: str | None = None,
        config_file: str = "config.toml",
        **kwargs,
    ) -> None:
        # List annotations for all configuration variables
        _annotations = {
            k: v
            for k, v in get_type_hints(self.__class__).items()
            if not k.startswith("_") and k.lower() == k
        }

        # Load configuration variables from TOML file
        if os.path.exists(config_file):
            for k, v in tomllib.load(open(config_file, "b")).items():
                if k in _annotations:
                    setattr(self, k, v)
                else:
                    raise KeyError(f"Unknown configuration variable: {k}")

        # Load configuration variables from environment variables
        for k, v in os.environ.items():
            k = k.lower()
            if k in _annotations:
                setattr(self, k, try_load_from_env_var(v, _annotations[k]))

        # Parse docstring to get help messages for configuration variables
        docstring = self.__class__.__doc__
        fields_help = try_parse_docstring(docstring, list(_annotations.keys()))

        # Load configuration variables from command line arguments
        parser = argparse.ArgumentParser()
        if parser_prog is not None:
            parser.prog = parser_prog
        for k, v in _annotations.items():
            opt_name = f"--{k.lower().replace('_', '-')}"
            field_help = fields_help.get(k, None)
            if v in (int, float, str):
                parser.add_argument(opt_name, type=v, help=field_help)
            elif v is bool:
                parser.add_argument(opt_name, action="store_true", help=field_help)
            elif get_origin(v) is Literal:
                parser.add_argument(opt_name, type=type(get_args(v)[0]), help=field_help)
            else:
                raise TypeError(f"Unsupported type: {v}")
        args = parser.parse_args()
        for k, v in vars(args).items():
            if v is None:
                continue
            _type = _annotations[k]
            if get_origin(_type) is Literal:
                if v not in get_args(_type):
                    raise ValueError(f"Invalid value: {v}")
            setattr(self, k, v)

        # Load configuration variables from override dictionary
        for k, v in kwargs.items():
            if k in _annotations:
                setattr(self, k, v)
            else:
                raise KeyError(f"Unknown configuration variable: {k}")
