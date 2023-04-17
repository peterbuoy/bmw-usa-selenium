FROM python:3.10.4-slim-buster

# Create and activate virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN source /venv/bin/activate

# Install dependencies
RUN apt-get update && \
    apt-get install -y chromium-driver && \
    rm -rf /var/lib/apt/lists/*
# Install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["python3", "main.py"]


WORKDIR /app




