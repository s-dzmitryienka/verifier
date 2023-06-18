FROM python:3.11.4-slim-bullseye as python-base

# Define ARGs
ARG ENVIRONMENT=default

# python vars
ENV PYTHONUNBUFFERED=1 \
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
    POETRY_VERSION=1.4.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN set -x \
    && buildDeps=" \
    libffi-dev \
    libpq-dev \
    gcc \
    python3-dev \
    binutils \
    build-essential \
    openssh-client \
    git \
    libproj-dev \
    gdal-bin \
    apt-transport-https \
    ca-certificates \
    curl \
    " \
    && runDeps=" \
    locales \
    " \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $buildDeps \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $runDeps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-root

# `final` image used for runtime
FROM python-base as final
ENV APP_ENV=local
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src /app/
WORKDIR /app
CMD ["uvicorn", "--reload", "main:app"]
