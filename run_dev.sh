#!/usr/bin/env bash
set -e

echo "==================================================================="
echo "    FORFRIEND — NỀN TẢNG TÌM BẠN HỌC (COURSE PROJECT DEMO)"
echo "         100% Pure Python Stack — Zero External Services"
echo "==================================================================="

# 1. Kích hoạt môi trường virtualenv
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "backend/.venv/bin/activate" ]; then
    source backend/.venv/bin/activate
fi

# 2. Khởi tạo database nếu chưa có
if [ ! -f "backend/forfriend.db" ]; then
    echo "[INFO] Khởi tạo database SQLite và nạp danh mục mẫu..."
    (cd backend && python -m app.init_db)
fi

# 3. Khởi chạy đồng thời Backend và Frontend
echo "[1/2] Khởi động Backend FastAPI (Port 8000)..."
(cd backend && python -m uvicorn app.main:app --reload --port 8000) &
BE_PID=$!

sleep 3

echo "[2/2] Khởi động Frontend Reflex (Port 3000)..."
(cd frontend && reflex run) &
FE_PID=$!

trap "kill $BE_PID $FE_PID 2>/dev/null" EXIT

echo ""
echo "==================================================================="
echo " Hệ thống ForFriend đã sẵn sàng:"
echo "   - Trang chủ Web Game (Frontend):  http://localhost:3000"
echo "   - Tài liệu API tương tác (Swagger): http://localhost:8000/docs"
echo "   - Database SQLite cục bộ:          backend/forfriend.db"
echo "==================================================================="
echo ""

wait
