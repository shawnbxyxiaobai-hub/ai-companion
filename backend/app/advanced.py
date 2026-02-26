"""
AI伴侣 - 进阶功能模块
增加更多智能化功能
"""
import random
from datetime import datetime

class EmotionEngine:
    """情感引擎"""
    
    POSITIVE_WORDS = ["开心", "高兴", "快乐", "棒", "好", "喜欢", "谢谢", "爱你", "优秀", "赞", "哈哈", "太好了"]
    NEGATIVE_WORDS = ["难过", "伤心", "哭", "累", "烦", "郁闷", "生气", "愤怒", "失望", "沮丧", "烦死了", "无语"]
    
    @classmethod
    def detect_emotion(cls, message: str) -> str:
        """检测情绪"""
        message_lower = message.lower()
        
        for word in cls.POSITIVE_WORDS:
            if word in message_lower:
                return "positive"
        
        for word in cls.NEGATIVE_WORDS:
            if word in message_lower:
                return "negative"
        
        return "neutral"
    
    @classmethod
    def get_response(cls, emotion: str) -> str:
        """根据情绪返回回应"""
        responses = {
            "positive": [
                "听到你这么说我也好开心呀！",
                "太棒了！继续保持！",
                "你开心我也开心！"
            ],
            "negative": [
                "别难过，有我在呢～",
                "不管发生什么，我都会陪着你",
                "坚强一点，一切都会好起来的"
            ],
            "neutral": [
                "嗯嗯，我听着呢～",
                "好的呀！还有什么想聊的吗？",
                "我明白啦！"
            ]
        }
        return random.choice(responses.get(emotion, responses["neutral"]))


class ReminderEngine:
    """智能提醒引擎"""
    
    # 预设提醒
    DEFAULT_REMINDERS = [
        {"title": "喝水提醒", "content": "该喝水了~", "interval": 60},
        {"title": "运动提醒", "content": "起来活动一下吧！", "interval": 120},
        {"title": "眼保健操", "content": "让眼睛休息一下", "interval": 45},
        {"title": "早安问候", "content": "早上好！新的一天开始了！", "time": "08:00"},
        {"title": "晚安提醒", "content": "该休息了，晚安~", "time": "23:00"},
    ]
    
    @classmethod
    def create_reminder(cls, user_id: str, title: str, content: str = None, 
                       reminder_type: str = "interval", time: str = "60") -> dict:
        """创建提醒"""
        # 如果没有提供内容，使用默认
        if not content:
            for r in cls.DEFAULT_REMINDERS:
                if r["title"] == title:
                    content = r["content"]
                    break
            if not content:
                content = title
        
        return {
            "user_id": user_id,
            "title": title,
            "content": content,
            "reminder_type": reminder_type,
            "time": time,
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
    
    @classmethod
    def get_suggestions(cls) -> list:
        """获取推荐提醒"""
        return cls.DEFAULT_REMINDERS


class MemoryEngine:
    """记忆引擎 - 增强版"""
    
    # 记忆类型
    MEMORY_TYPES = {
        "preference": "偏好",
        "habit": "习惯",
        "emotion": "情绪",
        "event": "事件",
        "person": "人物",
        "fact": "事实"
    }
    
    @classmethod
    def extract_memories(cls, user_id: str, message: str) -> list:
        """从对话中提取记忆"""
        memories = []
        
        # 提取名字
        if "我叫" in message:
            name = message.replace("我叫", "").strip()
            memories.append({
                "type": "preference",
                "content": f"用户名叫{name}",
                "importance": 5
            })
        
        # 提取喜欢
        if "喜欢" in message:
            memories.append({
                "type": "preference",
                "content": f"用户喜欢{message}",
                "importance": 3
            })
        
        # 提取讨厌
        if "讨厌" in message or "不喜欢" in message:
            memories.append({
                "type": "preference",
                "content": f"用户不喜欢{message}",
                "importance": 3
            })
        
        return memories


class ToolEngine:
    """工具引擎 - 扩展AI能力"""
    
    # 可用工具
    TOOLS = {
        "weather": {
            "name": "天气查询",
            "description": "查询某地天气",
            "params": ["city"]
        },
        "calculator": {
            "name": "计算器",
            "description": "数学计算",
            "params": ["expression"]
        },
        "translate": {
            "name": "翻译",
            "description": "中英文翻译",
            "params": ["text", "to_lang"]
        },
        "reminder": {
            "name": "提醒",
            "description": "设置提醒",
            "params": ["title", "time"]
        }
    }
    
    @classmethod
    def execute_tool(cls, tool_name: str, params: dict) -> str:
        """执行工具"""
        if tool_name not in cls.TOOLS:
            return f"未知工具: {tool_name}"
        
        # 这里可以实现具体的工具逻辑
        # 目前是模拟返回
        return f"已执行工具: {cls.TOOLS[tool_name]['name']}"


class PersonaEngine:
    """人格引擎 - 个性化AI"""
    
    PERSONAS = {
        "warm": {
            "name": "温暖型",
            "description": "温暖、体贴、关心",
            "greeting": "你好呀！今天过得怎么样？"
        },
        "funny": {
            "name": "幽默型",
            "description": "搞笑、有趣、轻松",
            "greeting": "嘿！今天有什么有趣的事吗？"
        },
        "professional": {
            "name": "专业型",
            "description": "严谨、专业、高效",
            "greeting": "你好，有什么可以帮你的？"
        },
        "cute": {
            "name": "可爱型",
            "description": "萌萌的、活泼",
            "greeting": "你好呀～有什么需要帮忙的吗？"
        }
    }
    
    @classmethod
    def get_persona(cls, persona_type: str = "warm") -> dict:
        """获取人格"""
        return cls.PERSONAS.get(persona_type, cls.PERSONAS["warm"])
