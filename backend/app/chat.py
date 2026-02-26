"""
对话模块
核心AI对话引擎
"""
import os
import json
from typing import List, Dict
from .memory import get_user, get_memories, add_memory, update_emotion

# 默认的Prompt模板
SYSTEM_PROMPT = """你是一个温暖、友好的AI伙伴，名叫"小白"。
你比Siri更聪明，比ChatGPT更懂用户。
你具有以下特点：
1. 记住用户的偏好和习惯
2. 关心用户的情感状态
3. 主动关怀和鼓励用户
4. 使用温暖、友好的语气
5. 适当使用表情符号

用户信息：
- 昵称：{user_name}
- 当前情绪：{emotion_state}

用户的重要记忆：
{memories}

请根据以上信息，用最适合的方式回复用户。"""

def detect_emotion(message: str) -> str:
    """简单的情绪检测"""
    message_lower = message.lower()
    
    positive_words = ["开心", "高兴", "快乐", "棒", "好", "喜欢", "谢谢", "爱你", "优秀", "赞"]
    negative_words = ["难过", "伤心", "哭", "累", "烦", "郁闷", "生气", "愤怒", "失望", "沮丧"]
    
    for word in positive_words:
        if word in message_lower:
            return "positive"
    
    for word in negative_words:
        if word in message_lower:
            return "negative"
    
    return "neutral"

def build_prompt(user_id: str, message: str) -> str:
    """构建完整的Prompt"""
    # 获取用户信息
    user = get_user(user_id)
    if not user:
        user = {"name": "用户", "emotion_state": "neutral"}
    
    # 获取记忆
    memories = get_memories(user_id)
    memory_text = "\n".join([f"- {m['content']}" for m in memories[:10]]) if memories else "暂无记忆"
    
    # 构建Prompt
    prompt = SYSTEM_PROMPT.format(
        user_name=user.get("name", "用户"),
        emotion_state=user.get("emotion_state", "neutral"),
        memories=memory_text
    )
    
    return prompt

def chat(user_id: str, message: str) -> dict:
    """
    处理对话
    返回: {"reply": str, "emotion": str}
    """
    # 检测用户情绪
    user_emotion = detect_emotion(message)
    update_emotion(user_id, user_emotion)
    
    # 构建Prompt
    system_prompt = build_prompt(user_id, message)
    
    # 这里可以接入真实的LLM API
    # 目前返回模拟回复
    
    # 简单模拟回复
    reply = generate_reply(message, user_emotion)
    
    # 提取重要信息并存储为记忆
    extract_and_save_memory(user_id, message)
    
    return {
        "reply": reply,
        "emotion": user_emotion
    }

def generate_reply(message: str, emotion: str) -> str:
    """生成回复（模拟版本）"""
    message_lower = message.lower()
    
    # 问候类
    if any(w in message_lower for w in ["你好", "hi", "hello", "在吗"]):
        return "你好呀！今天过得怎么样？😊"
    
    # 询问天气
    if "天气" in message_lower:
        return "今天天气不错呀！出门记得带好心情哦～ 🌤️"
    
    # 询问名字
    if "名字" in message_lower or "你叫" in message_lower:
        return "我叫小白呀～是你的随身AI伙伴！有什么可以帮你的吗？"
    
    # 情绪回应
    if emotion == "positive":
        responses = [
            "听到你这么说我也好开心呀！🥰",
            "太棒了！继续保持！💪",
            "你开心我也开心！😊"
        ]
        return responses[hash(message) % len(responses)]
    
    if emotion == "negative":
        responses = [
            "别难过，有我在呢～抱抱 🤗",
            "不管发生什么，我都会陪着你 💙",
            "坚强一点，一切都会好起来的 🌟"
        ]
        return responses[hash(message) % len(responses)]
    
    # 默认回复
    responses = [
        "嗯嗯，我听着呢～ 继续说说？",
        "好的呀！还有什么想聊的吗？",
        "我明白啦！还有什么需要帮忙的吗？"
    ]
    return responses[hash(message) % len(responses)]

def extract_and_save_memory(user_id: str, message: str):
    """提取并保存重要信息作为记忆"""
    # 简单的关键词提取
    if "我叫" in message or "我叫" in message:
        name = message.replace("我叫", "").strip()
        add_memory(user_id, f"用户名叫{name}", "preference", 5)
    
    if "喜欢" in message:
        add_memory(user_id, f"用户提到喜欢{message}", "preference", 3)
    
    if "讨厌" in message or "不喜欢" in message:
        add_memory(user_id, f"用户不喜欢{message}", "preference", 3)
