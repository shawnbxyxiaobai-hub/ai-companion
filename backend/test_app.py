"""
随身AI伙伴 - 测试用例

运行方式: pytest test_app.py -v
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.chat import chat, detect_emotion, generate_reply
from app.memory import get_user, create_user, add_memory, get_memories

client = TestClient(app)

# ==================== 对话接口测试 ====================

class TestChat:
    """对话模块测试"""
    
    def test_chat_basic(self):
        """测试基本对话"""
        response = client.post(
            "/api/chat",
            json={"user_id": "test_user", "message": "你好"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert "emotion" in data
        assert len(data["reply"]) > 0
    
    def test_chat_with_name(self):
        """测试询问名字"""
        response = client.post(
            "/api/chat",
            json={"user_id": "test_user", "message": "你叫什么名字？"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "小白" in data["reply"] or "名字" in data["reply"]
    
    def test_chat_weather(self):
        """测试询问天气"""
        response = client.post(
            "/api/chat",
            json={"user_id": "test_user", "message": "今天天气怎么样？"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "天气" in data["reply"] or "weather" in data["reply"].lower()

# ==================== 情绪检测测试 ====================

class TestEmotion:
    """情绪检测测试"""
    
    def test_positive_emotion(self):
        """测试积极情绪检测"""
        emotion = detect_emotion("我今天好开心啊！")
        assert emotion == "positive"
    
    def test_negative_emotion(self):
        """测试消极情绪检测"""
        emotion = detect_emotion("我很难过，想哭")
        assert emotion == "negative"
    
    def test_neutral_emotion(self):
        """测试中性情绪检测"""
        emotion = detect_emotion("明天天气怎么样？")
        assert emotion == "neutral"

# ==================== 记忆模块测试 ====================

class TestMemory:
    """记忆模块测试"""
    
    def test_create_user(self):
        """测试创建用户"""
        user_id = "test_memory_user"
        user = create_user(user_id, "测试用户")
        assert user["user_id"] == user_id
        assert user["name"] == "测试用户"
    
    def test_add_memory(self):
        """测试添加记忆"""
        user_id = "test_memory_user2"
        create_user(user_id)
        
        memory = add_memory(user_id, "用户喜欢打篮球", "preference", 4)
        assert memory["content"] == "用户喜欢打篮球"
        assert memory["memory_type"] == "preference"
    
    def test_get_memories(self):
        """测试获取记忆"""
        user_id = "test_memory_user3"
        create_user(user_id)
        
        add_memory(user_id, "记忆1", "preference", 3)
        add_memory(user_id, "记忆2", "habit", 4)
        
        memories = get_memories(user_id)
        assert len(memories) >= 2
        
        preference_memories = get_memories(user_id, "preference")
        assert all(m["memory_type"] == "preference" for m in preference_memories)

# ==================== 用户接口测试 ====================

class TestUser:
    """用户接口测试"""
    
    def test_get_nonexistent_user(self):
        """测试获取不存在的用户"""
        response = client.get("/api/user/nonexistent_user_12345")
        assert response.status_code == 404
    
    def test_create_user(self):
        """测试创建用户"""
        response = client.post(
            "/api/user/new_user_123",
            params={"name": "新用户"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["name"] == "新用户"

# ==================== 提醒接口测试 ====================

class TestReminder:
    """提醒接口测试"""
    
    def test_create_reminder(self):
        """测试创建提醒"""
        response = client.post(
            "/api/reminder/reminder_test_user",
            params={
                "title": "喝水提醒",
                "content": "该喝水了",
                "reminder_type": "interval",
                "time": "60"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["reminder"]["title"] == "喝水提醒"
    
    def test_get_reminders(self):
        """测试获取提醒"""
        # 先创建提醒
        client.post(
            "/api/reminder/reminder_test_user2",
            params={
                "title": "测试提醒",
                "content": "测试内容",
                "reminder_type": "fixed",
                "time": "09:00"
            }
        )
        
        # 获取提醒
        response = client.get("/api/reminder/reminder_test_user2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["reminders"]) > 0

# ==================== 健康检查测试 ====================

class TestHealth:
    """健康检查测试"""
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
