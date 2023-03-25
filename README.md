# Lightning7 - SSL Software

This repository contains Lightning7's (TU Delft RSA) software for the RoboCup Small Size League.

## Development Kickstart

1. Make sure you have at least Python 3.9 (you can use [pyenv](https://github.com/pyenv/pyenv))
2. Install [poetry](https://python-poetry.org/docs/#installation)
3. Run `poetry install` to download all the dependencies into a virtual environment
4. (*Optional*) Enter the newly created virtual env with `poetry shell`

To add a dependency:
```bash
poetry add requests
```

## Repository structure

Currently, the whole repository is made up of a single [poetry](https://python-poetry.org/) package.

 - `lightning7-ssl` - the main Python module
   - `stratcore` - the core of strategy framework
   - ... other modules go here
 - `test` - place for package-wide unit tests
 - `pyproject.toml` - package config, see [the poetry docs](https://python-poetry.org/docs/pyproject/) and the [pip docs](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)
 - `poetry.lock` - dependency lock, should not be touched manually

## Licensing

The contents of this repository are licensed under *TODO*
