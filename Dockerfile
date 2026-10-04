# ==========================================
# ForFriend - Unified Production Container
# FastAPI + Reflex + SQLite + Caddy Reverse Proxy
# ==========================================

FROM caddy:2.8.4-alpine AS caddy-stage
FROM oven/bun:1.1-slim AS bun-stage

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=10000 \
    REFLEX_API_URL="" \
    BACKEND_URL="http://127.0.0.1:8000"

# Install system dependencies, Node.js and utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    unzip \
    ca-certificates \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy Caddy reverse proxy and Bun binary
COPY --from=caddy-stage /usr/bin/caddy /usr/bin/caddy
COPY --from=bun-stage /usr/local/bin/bun /usr/local/bin/bun

WORKDIR /app

# Install Python backend and frontend dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
COPY frontend/requirements.txt /app/frontend/requirements.txt

RUN pip install --no-cache-dir -r /app/backend/requirements.txt && \
    pip install --no-cache-dir -r /app/frontend/requirements.txt

# Copy source code
COPY . /app

# Ensure executable permissions and line endings on startup script
RUN chmod +x /app/start.sh

# Pre-initialize Reflex frontend
WORKDIR /app/frontend
RUN reflex init && \
    python patch_react_router.py || true

WORKDIR /app

# Expose Render standard container port
EXPOSE 10000

CMD ["/bin/bash", "/app/start.sh"]
