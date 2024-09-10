FROM python:3.11-slim-bullseye

WORKDIR /app/

# # Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    gcc \
    libc-dev \
    libffi-dev \
    libpq-dev \
    postgresql-client \
    redis-tools \
    netcat \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create logs directory
RUN mkdir -p /logs

# Install python dependencies
COPY requirements.txt /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the source code
COPY . /app/
