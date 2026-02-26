"""
API扩展模块
增加更多接口
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .advanced import EmotionEngine, ReminderEngine, MemoryEngine, ToolEngine, PersonaEngine

router = APIRouter()

# ==================== 情感接口 ====================

class EmotionRequest(BaseModel):
    user_id: str
    message: str

@router.post("/api/emotion/detect")
async def detect_emotion(request: EmotionRequest):
    """情绪检测接口"""
    emotion = EmotionEngine.detect_emotion(request.message)
    response = EmotionEngine.get_response(emotion)
    return {
        "emotion": emotion,
        "response": response
    }

# ==================== 提醒建议接口 ====================

@router.get("/api/reminder/suggestions")
async def get_reminder_suggestions():
    """获取推荐提醒"""
    suggestions = ReminderEngine.get_suggestions()
    return {"suggestions": suggestions}

# ==================== 工具接口 ====================

class ToolRequest(BaseModel):
    tool_name: str
    params: dict = {}

@router.post("/api/tool/execute")
async def execute_tool(request: ToolRequest):
    """执行工具"""
    result = ToolEngine.execute_tool(request.tool_name, request.params)
    return {"result": result}

@router.get("/api/tools")
async def list_tools():
    """列出所有可用工具"""
    return {"tools": ToolEngine.TOOLS}

# ==================== 人格接口 ====================

@router.get("/api/persona/{persona_type}")
async def get_persona(persona_type: str = "warm"):
    """获取人格设置"""
    persona = PersonaEngine.get_persona(persona_type)
    return persona

@router.get("/api/personas")
async def list_personas():
    """列出所有可用人格"""
    return {"personas": PersonaEngine.PERSONAS}

# ==================== 记忆提取接口 ====================

class ExtractRequest(BaseModel):
    user_id: str
    message: str

@router.post("/api/memory/extract")
async def extract_memory(request: ExtractRequest):
    """从消息中提取记忆"""
    memories = MemoryEngine.extract_memories(request.user_id, request.message)
    return {"extracted": memories}

# ==================== 统计接口 ====================

@router.get("/api/stats/{user_id}")
async def get_user_stats(user_id: str):
    """获取用户统计信息"""
    from .memory import get_memories, get_reminders
    
    memories = get_memories(user_id)
    reminders = get_reminders(user_id)
    
    return {
        "user_id": user_id,
        "memory_count": len(memories),
        "reminder_count": len(reminders),
        "active_reminders": len([r for r in reminders if r.get("enabled", False)])
    }
