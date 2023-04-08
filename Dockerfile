FROM python:3.10.10-alpine

ENV POETRY_HOME=/opt/poetry

# Install git, curl, zip, nodejs, poetry, pnpm
RUN apk add --no-cache --update-cache gcc gfortran build-base wget freetype-dev libpng-dev openblas-dev git curl zip nodejs npm && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VERSION=1.4.1 python3 - && \
    npm install -g pnpm

# Move to /app
WORKDIR /app

# Copy the requirements file
COPY pyproject.toml poetry.lock ./

# Install python dependencies
RUN mkdir -p ./lightning7_ssl && touch ./lightning7_ssl/__init__.py && touch README.md && $POETRY_HOME/bin/poetry install --without dev

# Copy the package.json and pnpm-lock.yaml file
COPY lightning7_ssl/web/frontend/package.json lightning7_ssl/web/frontend/pnpm-lock.yaml ./lightning7_ssl/web/frontend/

# Install node dependencies
RUN cd lightning7_ssl/web/frontend && pnpm install

# Copy the rest of the code
COPY . .

ENTRYPOINT [ "/bin/sh", "-c" ]
CMD ["/opt/poetry/bin/poetry run python -m lightning7_ssl --ui"]
