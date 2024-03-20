FROM python:3.10-slim-bullseye as base

# Adapted from https://github.com/python-poetry/poetry/discussions/1879#discussioncomment-216865
ENV \
    # python
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.4.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    BUILDER_PATH="/builder" \
    VENV_PATH="/builder/.venv"

# Set up path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install nodemon for test watching
RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/* \
    && npm i -g nodemon

FROM base as builder

# Install poetry - respects $POETRY_VERSION, etc...
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org/ | python - \
    \
    # Remove curl
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry.lock and pyproject.toml
WORKDIR $BUILDER_PATH
COPY poetry.lock pyproject.toml ./

# Install Python packages
RUN --mount=type=cache,target=/builder/.venv \
    poetry install --sync \
    && cp -rT $VENV_PATH $VENV_PATH-out

FROM base as main

# Copy virtual environment
COPY --from=builder $VENV_PATH-out $VENV_PATH

# Switch to non-root user
RUN useradd -m -u 1000 -o -s /bin/bash user
USER user

WORKDIR /app

# Start the container and do nothing
CMD ["nodemon", "tail", "-f", "/dev/null"]