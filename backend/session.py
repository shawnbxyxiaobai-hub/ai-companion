"""
会话管理
管理用户会话
"""
import uuid
import time
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

class Session:
    """会话"""
    
    def __init__(self, user_id: str, session_id: str = None, ttl: int = 3600):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = time.time()
        self.last_active = time.time()
        self.ttl = ttl
        self.data = {}
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() - self.last_active > self.ttl
    
    def update_activity(self):
        """更新活跃时间"""
        self.last_active = time.time()
    
    def set(self, key: str, value: Any):
        """设置会话数据"""
        self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取会话数据"""
        return self.data.get(key, default)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": datetime.fromtimestamp(self.created_at).isoformat(),
            "last_active": datetime.fromtimestamp(self.last_active).isoformat(),
            "ttl": self.ttl,
            "data": self.data
        }


class SessionManager:
    """会话管理器"""
    
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self.sessions: Dict[str, Session] = {}
    
    def create_session(self, user_id: str, session_id: str = None) -> Session:
        """创建会话"""
        session = Session(user_id, session_id, self.default_ttl)
        self.sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        session = self.sessions.get(session_id)
        
        if session and session.is_expired():
            self.delete_session(session_id)
            return None
        
        return session
    
    def update_session(self, session_id: str) -> bool:
        """更新会话活跃时间"""
        session = self.get_session(session_id)
        if session:
            session.update_activity()
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_user_sessions(self, user_id: str) -> list:
        """获取用户的所有会话"""
        return [
            s for s in self.sessions.values() 
            if s.user_id == user_id and not s.is_expired()
        ]
    
    def cleanup_expired(self) -> int:
        """清理过期会话"""
        expired = [
            sid for sid, s in self.sessions.items() 
            if s.is_expired()
        ]
        
        for sid in expired:
            del self.sessions[sid]
        
        return len(expired)
    
    def get_stats(self) -> Dict:
        """获取会话统计"""
        return {
            "total_sessions": len(self.sessions),
            "active_users": len(set(s.user_id for s in self.sessions.values() if not s.is_expired())),
            "expired_sessions": len([s for s in self.sessions.values() if s.is_expired()])
        }


# 全局会话管理器
session_manager = SessionManager()


# 使用示例
if __name__ == "__main__":
    # 创建会话
    session = session_manager.create_session("user123")
    print(f"创建会话: {session.session_id}")
    
    # 设置会话数据
    session.set("name", "张三")
    session.set("persona", "warm")
    
    # 获取会话
    s = session_manager.get_session(session.session_id)
    print(f"用户: {s.user_id}")
    print(f"名字: {s.get('name')}")
    
    # 统计
    print(f"\n会话统计: {session_manager.get_stats()}")
    
    # 清理
    cleaned = session_manager.cleanup_expired()
    print(f"清理过期会话: {cleaned}")
