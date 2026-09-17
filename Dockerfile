FROM nikolaik/python-nodejs:python3.14-nodejs26-slim

# Install system dependencies and clean up apt cache to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install mystmd globally
RUN npm install -g mystmd

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt