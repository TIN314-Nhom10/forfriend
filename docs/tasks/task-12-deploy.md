# Task 12 — Deployment & DevOps

## Mục tiêu
Chuẩn bị production deployment: Docker multi-stage build, environment config, Nginx reverse proxy, CI/CD cơ bản, và hướng dẫn deploy.

## Phụ thuộc
- Tất cả tasks 01–11 hoàn thành

## Yêu cầu chi tiết

### 12.1. Docker Multi-stage Build

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### 12.2. Nginx Config

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket proxy
    location /ws/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Static uploads
    location /uploads/ {
        proxy_pass http://backend:8000;
    }

    # Gzip
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
}
```

### 12.3. Production Docker Compose

`docker-compose.prod.yml`:
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      LIVEKIT_API_KEY: ${LIVEKIT_API_KEY}
      LIVEKIT_API_SECRET: ${LIVEKIT_API_SECRET}
      LIVEKIT_URL: ${LIVEKIT_URL}
    depends_on:
      - db
      - redis
    volumes:
      - uploads:/app/uploads
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    restart: always

volumes:
  pgdata:
  uploads:
```

### 12.4. Environment Files

`.env.example`:
```bash
# Database
POSTGRES_DB=studybuddy
POSTGRES_USER=postgres
POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD

# JWT
JWT_SECRET_KEY=CHANGE_ME_RANDOM_STRING_64_CHARS

# LiveKit
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_URL=wss://your-project.livekit.cloud

# App
CORS_ORIGINS=["https://your-domain.com"]
```

### 12.5. Startup Script

`scripts/deploy.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 StudyBuddy Deployment"

# 1. Pull latest
git pull origin main

# 2. Build images
docker-compose -f docker-compose.prod.yml build

# 3. Run migrations
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head

# 4. Seed data (if first deploy)
docker-compose -f docker-compose.prod.yml run --rm backend python -m app.seed

# 5. Start services
docker-compose -f docker-compose.prod.yml up -d

echo "✅ Deployment complete!"
```

### 12.6. Health Check

Thêm health check vào Docker Compose:
```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

### 12.7. README.md

Viết README hoàn chỉnh:
- Project description
- Tech stack
- Prerequisites (Docker, Node, Python)
- Quick start (development)
- Environment variables
- API documentation link (/docs)
- LiveKit setup guide
- Production deployment
- Contributing guide

## Tiêu chí hoàn thành

- [ ] Docker multi-stage build cho cả BE + FE
- [ ] `docker-compose -f docker-compose.prod.yml up` chạy thành công
- [ ] Nginx proxy đúng: API, WebSocket, Static files
- [ ] Alembic migration chạy trong Docker
- [ ] Health check hoạt động
- [ ] README.md đầy đủ
- [ ] `.env.example` có tất cả biến cần thiết
- [ ] Deploy script hoạt động
