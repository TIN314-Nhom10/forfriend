#!/bin/bash
set -e

echo "=========================================================="
echo "    FORFRIEND — Launching Cloud Production Stack"
echo "=========================================================="

PORT="${PORT:-10000}"
export PORT

# 1. Initialize SQLite Database & seed categories
echo "[1/3] Initializing SQLite database..."
cd /app/backend
python -m app.init_db

# 2. Start FastAPI Backend on internal port 8000
echo "[2/3] Starting FastAPI Backend on 127.0.0.1:8000..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 3. Start Reflex State Engine (Backend-only) on internal port 8001
echo "[3/3] Starting Reflex Backend on 127.0.0.1:8001..."
cd /app/frontend
export REFLEX_BACKEND_ONLY=1
reflex run --env prod --backend-only --backend-port 8001 &
REFLEX_PID=$!

# 4. Generate Nginx configuration from template with dynamic $PORT
echo "[4/4] Configuring Nginx reverse proxy on port $PORT..."
envsubst '${PORT}' < /app/nginx.conf.template > /tmp/nginx.conf

# Graceful termination handler
cleanup() {
    echo "Stopping services..."
    nginx -s stop 2>/dev/null || true
    kill -TERM "$BACKEND_PID" "$REFLEX_PID" 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

echo "=========================================================="
echo " ForFriend is LIVE on Render port $PORT!"
echo "   - Web App:      http://0.0.0.0:$PORT/"
echo "   - Swagger Docs: http://0.0.0.0:$PORT/docs"
echo "=========================================================="

# Start Nginx in foreground
exec nginx -c /tmp/nginx.conf -g "daemon off;"
