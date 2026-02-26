"""
缓存管理
提高性能
"""
import time
import json
from typing import Any, Optional, Dict
from functools import wraps
import hashlib

class Cache:
    """简单内存缓存"""
    
    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self._cache: Dict[str, tuple] = {}  # key -> (value, expire_time)
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self._cache:
            value, expire_time = self._cache[key]
            if expire_time > time.time():
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """设置缓存"""
        ttl = ttl or self.default_ttl
        expire_time = time.time() + ttl
        self._cache[key] = (value, expire_time)
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """检查是否存在"""
        return self.get(key) is not None
    
    def size(self) -> int:
        """缓存大小"""
        # 清理过期项
        now = time.time()
        self._cache = {
            k: v for k, v in self._cache.items() 
            if v[1] > now
        }
        return len(self._cache)


# 全局缓存实例
cache = Cache()


def cached(ttl: int = 300, key_prefix: str = ""):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存key
            key_args = json.dumps(args, sort_keys=True) + json.dumps(kwargs, sort_keys=True)
            key = f"{key_prefix}{func.__name__}:{hashlib.md5(key_args.encode()).hexdigest()}"
            
            # 尝试从缓存获取
            result = cache.get(key)
            if result is not None:
                return result
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            cache.set(key, result, ttl)
            
            return result
        return wrapper
    return decorator


class RedisCache:
    """Redis缓存 (可选)"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._client = None
    
    def get_client(self):
        """获取Redis客户端"""
        if self._client is None:
            try:
                import redis
                self._client = redis.from_url(self.redis_url)
            except ImportError:
                return None
        return self._client
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        client = self.get_client()
        if not client:
            return None
        
        try:
            value = client.get(key)
            if value:
                return json.loads(value)
        except:
            pass
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        """设置缓存"""
        client = self.get_client()
        if not client:
            return
        
        try:
            client.setex(key, ttl, json.dumps(value))
        except:
            pass


# 使用示例
if __name__ == "__main__":
    # 测试内存缓存
    cache.set("test", "hello", 10)
    print(f"获取缓存: {cache.get('test')}")
    print(f"缓存大小: {cache.size()}")
    
    # 测试装饰器
    @cached(ttl=60, key_prefix="test:")
    def slow_function(x):
        time.sleep(1)
        return x * 2
    
    print("第一次调用:")
    start = time.time()
    print(slow_function(5))
    print(f"耗时: {time.time() - start:.2f}s")
    
    print("第二次调用(缓存):")
    start = time.time()
    print(slow_function(5))
    print(f"耗时: {time.time() - start:.2f}s")
