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

# 3. Start Reflex Frontend on internal port 3000
echo "[3/3] Starting Reflex Frontend on 127.0.0.1:3000..."
cd /app/frontend
python patch_react_router.py || true
reflex run --env prod --frontend-port 3000 &
FRONTEND_PID=$!

# Graceful termination handler
cleanup() {
    echo "Stopping services..."
    kill -TERM "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

# 4. Start Caddy Reverse Proxy on Render's assigned $PORT
echo "=========================================================="
echo " ForFriend is LIVE on Render port $PORT!"
echo "   - Web App:      http://0.0.0.0:$PORT/"
echo "   - Swagger Docs: http://0.0.0.0:$PORT/docs"
echo "=========================================================="
exec caddy run --config /app/Caddyfile --adapter caddyfile
