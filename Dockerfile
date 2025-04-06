# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install --upgrade -r packages.txt &&

# Set the virtual environment as the default Python
ENV PATH="/app/.venv/bin:$PATH"

# Run tests
CMD ["python", "main.test.py"]