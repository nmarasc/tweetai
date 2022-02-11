FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Add commit hash as an identifier
ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-debug}

# Update tools
RUN pip install -U \
    pip \
    setuptools \
    wheel

# Create project root
WORKDIR /app
COPY . /app

# Install dependencies
RUN python3 setup.py install

# Create non root user
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "start.py"]
