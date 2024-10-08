FROM python:3.11.9-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    wget \
    sqlite3 \
    libsqlite3-dev \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using pip
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -

# Copy project files
COPY pyproject.toml poetry.lock* /app/

# Project initialization:
RUN poetry install

# Copy the rest of the application code
COPY . /app

# Install additional dependencies for selenium and undetected-chromedriver
RUN poetry add selenium-wire undetected-chromedriver

# Set display port to avoid crash
ENV DISPLAY=:99

# Set the path to chromium
ENV CHROME_BIN=/usr/bin/chromium