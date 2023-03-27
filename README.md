# Lightning7 - SSL Software

This repository contains Lightning7's (TU Delft RSA) software for the RoboCup Small Size League.

## Development Kickstart

1. Make sure you have all dependencies:
   1. Python 3.9+ (you can use [pyenv](https://github.com/pyenv/pyenv) to change the version of Python you're using)
   2. Node.js 18+ (you can use [fnm](https://github.com/Schniz/fnm))
   3. [Poetry](https://python-poetry.org/docs/#installation)
   4. [PNPM](https://pnpm.io/installation)
2. Run `poetry install` to download all the dependencies into a virtual environment
3. Install the pre-commit hooks with `poetry run pre-commit install`
4. Run `cd lightning7_ssl/web/frontend && pnpm install` to download all the frontend dependencies
5. (*Optional*) Enter the newly created virtual env with `poetry shell`

To run the main program:
```bash
poetry run python -m lightning7_ssl
```

Available command-line arguments:
 - `--ui` - enable the web UI
 - `--log-file` - log file path (default: no logging)
 - `--num-players` - number of players (default: 11)
 - `--own-team` - own team color (default: blue)
 - `--tick-interval` - tick interval in seconds (default: 0.1)

Run the Python tests:
```bash
poetry run python -m unittest
```

Add a Python dependency:
```bash
poetry add ...
```

Add a frontend dependency (in `lightning7_ssl/web/frontend`):
```bash
pnpm add ...
```


## Overview

Currently, the whole repository is made up of a single [poetry](https://python-poetry.org/) package.

 - `lightning7-ssl` - the main Python module
   - `control_client` - client that talks to ssl-vision, ssl-game-controller and the robots, via protobuf
   - `player` - player and player manager classes (see strategy)
   - `roles` - role classes (see strategy)
   - `world` - world model
   - `web` - web UI server and frontend
     - `frontend/` - frontend code (vite + svelte)
     - `server` - backend code
   - `vis` - logging and visualization
   - `utils` - utility functions and classes
     - `vec_math` - vector math
   - ... other modules go here
 - `test` - place for package-wide unit tests
 - `pyproject.toml` - package config, see [the poetry docs](https://python-poetry.org/docs/pyproject/) and the [pip docs](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)
 - `poetry.lock` - dependency lock, should not be touched manually
 - `pre-commit-config.yaml` - pre-commit hooks config, see [the pre-commit docs](https://pre-commit.com/)

## Licensing

The contents of this repository are licensed under *TODO*
