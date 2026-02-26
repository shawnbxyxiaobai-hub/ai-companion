"""
性能监控
监控服务性能
"""
import time
import psutil
import os
from typing import Dict, Any
from datetime import datetime

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    def record_request(self):
        """记录请求"""
        self.request_count += 1
    
    def record_error(self):
        """记录错误"""
        self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "uptime_formatted": self._format_time(uptime),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / self.request_count if self.request_count > 0 else 0,
            "requests_per_second": self.request_count / uptime if uptime > 0 else 0
        }
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "process_count": len(psutil.pids())
        }


class RateLimiter:
    """限流器"""
    
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """检查是否允许请求"""
        now = time.time()
        
        # 清理过期记录
        self.requests = {
            uid: times 
            for uid, times in self.requests.items() 
            if times[-1] > now - self.window
        }
        
        # 检查限制
        if identifier in self.requests:
            times = [t for t in self.requests[identifier] if t > now - self.window]
            
            if len(times) >= self.max_requests:
                return False
            
            times.append(now)
            self.requests[identifier] = times
        else:
            self.requests[identifier] = [now]
        
        return True
    
    def get_remaining(self, identifier: str) -> int:
        """获取剩余请求数"""
        now = time.time()
        
        if identifier not in self.requests:
            return self.max_requests
        
        times = [t for t in self.requests[identifier] if t > now - self.window]
        return max(0, self.max_requests - len(times))


class CircuitBreaker:
    """断路器"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        """执行函数"""
        if self.state == "open":
            # 检查是否应该切换到half_open
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half_open"
            else:
                raise Exception("断路器打开")
        
        try:
            result = func(*args, **kwargs)
            
            # 成功
            if self.state == "half_open":
                self.state = "closed"
                self.failure_count = 0
            
            return result
        
        except Exception as e:
            # 失败
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            
            raise e
    
    def get_state(self) -> str:
        """获取状态"""
        return self.state


# 使用示例
if __name__ == "__main__":
    # 性能监控
    monitor = PerformanceMonitor()
    monitor.record_request()
    monitor.record_request()
    monitor.record_error()
    
    print("性能统计:")
    print(monitor.get_stats())
    print()
    print("系统统计:")
    print(monitor.get_system_stats())
    
    # 限流器
    limiter = RateLimiter(max_requests=5, window=60)
    
    for i in range(7):
        allowed = limiter.is_allowed("user1")
        print(f"请求 {i+1}: {'✅ 允许' if allowed else '❌ 拒绝'}")
        print(f"  剩余: {limiter.get_remaining('user1')}")
