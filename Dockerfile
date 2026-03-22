FROM ubuntu:latest
LABEL authors="Andrei Draghici"

FROM ubuntu:24.04

ARG APP_VERSION="1.0"
ARG APP_NAME="personal-website-1"

# Install dependencies and python3-venv for virtual environment
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# Create a working directory
WORKDIR /app

# Copy dependency file
COPY project/requirements.txt requirements.txt

# Create a virtual environment and install dependencies
RUN python3 -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r requirements.txt

# Copy remaining files
COPY project/ ./

# Create the output and logs directories
RUN mkdir -p /app/output /app/logs

# Set the entry point with output redirection
ENTRYPOINT ["sh", "-c", "venv/bin/python main.py > /app/logs/logfile.trc 2>&1"]