"""
进阶功能测试
"""
import pytest
from app.advanced import EmotionEngine, ReminderEngine, MemoryEngine, ToolEngine, PersonaEngine

class TestEmotionEngine:
    """情感引擎测试"""
    
    def test_positive_emotion(self):
        emotion = EmotionEngine.detect_emotion("我今天好开心啊！")
        assert emotion == "positive"
    
    def test_negative_emotion(self):
        emotion = EmotionEngine.detect_emotion("我很难过，想哭")
        assert emotion == "negative"
    
    def test_neutral_emotion(self):
        emotion = EmotionEngine.detect_emotion("明天天气怎么样？")
        assert emotion == "neutral"
    
    def test_get_response(self):
        response = EmotionEngine.get_response("positive")
        assert response is not None
        assert len(response) > 0


class TestReminderEngine:
    """提醒引擎测试"""
    
    def test_create_reminder(self):
        reminder = ReminderEngine.create_reminder(
            "user1", "测试提醒", "测试内容"
        )
        assert reminder["title"] == "测试提醒"
        assert reminder["content"] == "测试内容"
        assert reminder["enabled"] is True
    
    def test_get_suggestions(self):
        suggestions = ReminderEngine.get_suggestions()
        assert len(suggestions) > 0
        assert "title" in suggestions[0]


class TestMemoryEngine:
    """记忆引擎测试"""
    
    def test_extract_name(self):
        memories = MemoryEngine.extract_memories("user1", "我叫张三")
        assert len(memories) > 0
        assert memories[0]["type"] == "preference"
    
    def test_extract_preference(self):
        memories = MemoryEngine.extract_memories("user1", "我喜欢打篮球")
        assert len(memories) > 0


class TestToolEngine:
    """工具引擎测试"""
    
    def test_execute_unknown_tool(self):
        result = ToolEngine.execute_tool("unknown", {})
        assert "未知工具" in result
    
    def test_list_tools(self):
        tools = ToolEngine.TOOLS
        assert "weather" in tools
        assert "calculator" in tools


class TestPersonaEngine:
    """人格引擎测试"""
    
    def test_get_warm_persona(self):
        persona = PersonaEngine.get_persona("warm")
        assert persona["name"] == "温暖型"
    
    def test_get_funny_persona(self):
        persona = PersonaEngine.get_persona("funny")
        assert persona["name"] == "幽默型"
    
    def test_list_personas(self):
        personas = PersonaEngine.PERSONAS
        assert len(personas) == 4
        assert "warm" in personas
        assert "funny" in personas
        assert "professional" in personas
        assert "cute" in personas


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
