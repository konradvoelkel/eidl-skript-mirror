FROM nikolaik/python-nodejs:python3.14-nodejs26-slim

# Install system dependencies and clean up apt cache to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install mystmd globally (version pinned to match pyproject.toml dev group)
RUN npm install -g mystmd@1.10.1

# The HTML build does not execute notebooks, so no Python packages are needed yet.
# If notebook execution is added (myst build --execute), install the project
# dependencies here, e.g. via `uv export` to a requirements.txt.
