FROM python:3.9
ARG APP_PATH=/backend/
ARG poetry_version=1.2.0
ARG INSTALL_DEV=false
WORKDIR $APP_PATH

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH=$APP_PATH \
    PATH="/opt/poetry/bin:$PATH"
# install poetry
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y curl build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=${poetry_version} python3 - && \
    poetry config virtualenvs.create false

COPY ./poetry.lock ./pyproject.toml $APP_PATH
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root  ; else poetry install --no-root --no-dev ; fi"
COPY ./ $APP_PATH
