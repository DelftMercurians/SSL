FROM ubuntu:20.04

# Install gcc, git, curl, zip, and other dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential gcc gfortran wget libpng-dev git curl zip

# Install rye
RUN curl -sSf https://rye-up.com/get | RYE_VERSION=0.6.0 RYE_INSTALL_OPTION="--yes" bash && \
    echo 'source "$HOME/.rye/env"' >> ~/.bashrc

# Install node v19.x
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs

# Install pnpm
RUN npm install -g pnpm

# Move to /app
WORKDIR /app

# Copy the requirements file
COPY pyproject.toml requirements.lock .python-version ./

# Install python dependencies
RUN mkdir -p ./lightning7_ssl && touch ./lightning7_ssl/__init__.py && touch README.md && $HOME/.rye/shims/rye sync

# Copy the package.json and pnpm-lock.yaml file
COPY lightning7_ssl/web/frontend/package.json lightning7_ssl/web/frontend/pnpm-lock.yaml ./lightning7_ssl/web/frontend/

# Install node dependencies
RUN cd lightning7_ssl/web/frontend && pnpm install

# Copy the rest of the code
COPY . .

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["rye run python -m lightning7_ssl --ui"]
