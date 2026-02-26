"""
中间件
扩展FastAPI功能
"""
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """请求计时中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        logger.info(f"{request.method} {request.url.path}")
        
        response = await call_next(request)
        
        logger.info(f"Response: {response.status_code}")
        
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """认证中间件"""
    
    def __init__(self, app, whitelist: list = None):
        super().__init__(app)
        self.whitelist = whitelist or ["/health", "/docs", "/openapi.json"]
    
    async def dispatch(self, request: Request, call_next):
        # 白名单跳过
        if request.url.path in self.whitelist:
            return await call_next(request)
        
        # 这里可以添加认证逻辑
        # 例如检查token
        
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """限流中间件"""
    
    def __init__(self, app, max_requests: int = 100, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        now = time.time()
        
        # 清理过期记录
        self.requests = {
            ip: times 
            for ip, times in self.requests.items() 
            if times[-1] > now - self.window
        }
        
        # 检查请求数
        if client_ip in self.requests:
            times = self.requests[client_ip]
            times = [t for t in times if t > now - self.window]
            
            if len(times) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "请求过于频繁"}
                )
            
            times.append(now)
            self.requests[client_ip] = times
        else:
            self.requests[client_ip] = [now]
        
        return await call_next(request)


class CORSMiddleware(BaseHTTPMiddleware):
    """自定义CORS中间件"""
    
    def __init__(self, app, allowed_origins: list = None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or ["*"]
    
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return Response(
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                }
            )
        
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        
        return response
