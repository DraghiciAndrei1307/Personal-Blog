FROM ubuntu:latest
LABEL authors="Andrei Draghici"

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
COPY requirements.txt ./

# Create a virtual environment and install dependencies
RUN python3 -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r requirements.txt

# Copy remaining files
COPY project/ ./project

# Create the output and logs directories
RUN mkdir -p /app/output /app/logs

# Set the ENV variables

ENV FLASK_APP=project.main
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose Port
EXPOSE 5000

# Start Flask app
CMD ["/app/venv/bin/flask", "run", "--host=0.0.0.0", "--port=5000"]

