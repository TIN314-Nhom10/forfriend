# ==========================================
# ForFriend - Unified Production Container
# FastAPI + Reflex + SQLite + Nginx Reverse Proxy
# ==========================================

FROM oven/bun:1.1-slim AS bun-stage

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=10000 \
    REFLEX_API_URL="" \
    BACKEND_URL="http://127.0.0.1:8000"

# Install system dependencies, Nginx, gettext (for envsubst) and Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    unzip \
    ca-certificates \
    nginx \
    gettext-base \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy Bun binary from official image
COPY --from=bun-stage /usr/local/bin/bun /usr/local/bin/bun

WORKDIR /app

# Install Python backend and frontend dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
COPY frontend/requirements.txt /app/frontend/requirements.txt

RUN pip install --no-cache-dir -r /app/backend/requirements.txt && \
    pip install --no-cache-dir -r /app/frontend/requirements.txt

# Copy source code
COPY . /app

# Ensure executable permissions on startup script
RUN chmod +x /app/start.sh

# Pre-export Reflex frontend during build time
WORKDIR /app/frontend
RUN reflex export --frontend-only --no-zip

WORKDIR /app

# Expose Render standard container port
EXPOSE 10000

CMD ["/bin/bash", "/app/start.sh"]
