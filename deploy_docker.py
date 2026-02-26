"""
Docker部署配置
"""
import os

# Docker相关配置
DOCKERFILE = """
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY backend/ .
COPY *.py .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

DOCKER_COMPOSE = """
version: '3.8'

services:
  ai-companion:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - APP_ENV=production
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
"""

NGINX_CONFIG = """
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /app/static;
    }
}
"""

# 保存Docker文件
with open('Dockerfile', 'w', encoding='utf-8') as f:
    f.write(DOCKERFILE)

with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(DOCKER_COMPOSE)

with open('nginx.conf', 'w', encoding='utf-8') as f:
    f.write(NGINX_CONFIG)

print("Docker配置文件已生成!")
