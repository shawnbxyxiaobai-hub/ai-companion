"""
随身AI伙伴后端服务
FastAPI主入口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from .models import ChatRequest, ChatResponse, Reminder
from .chat import chat
from .memory import get_user, create_user, get_memories, add_memory
from .reminder import add_reminder, get_reminders, delete_reminder, toggle_reminder
from . import api扩展

# 注册扩展API
app.include_router(api扩展.router, prefix="", tags=["扩展功能"])

app = FastAPI(
    title="随身AI伙伴 API",
    description="比Siri更聪明、比ChatGPT更懂你的随身AI伙伴",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 对话接口 ====================

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """对话接口"""
    # 确保用户存在
    user = get_user(request.user_id)
    if not user:
        create_user(request.user_id)
    
    # 处理对话
    result = chat(request.user_id, request.message)
    return ChatResponse(**result)

# ==================== 用户接口 ====================

@app.get("/api/user/{user_id}")
async def get_user_info(user_id: str):
    """获取用户信息"""
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.post("/api/user/{user_id}")
async def create_user_endpoint(user_id: str, name: str = "用户"):
    """创建用户"""
    user = get_user(user_id)
    if user:
        return {"message": "用户已存在", "user": user}
    
    new_user = create_user(user_id, name)
    return {"message": "创建成功", "user": new_user}

# ==================== 记忆接口 ====================

@app.get("/api/memory/{user_id}")
async def get_user_memories(user_id: str, memory_type: Optional[str] = None):
    """获取用户记忆"""
    memories = get_memories(user_id, memory_type)
    return {"memories": memories}

@app.post("/api/memory/{user_id}")
async def add_user_memory(user_id: str, content: str, memory_type: str = "preference", importance: int = 3):
    """添加记忆"""
    memory = add_memory(user_id, content, memory_type, importance)
    return {"message": "添加成功", "memory": memory}

# ==================== 提醒接口 ====================

@app.get("/api/reminder/{user_id}")
async def get_user_reminders(user_id: str):
    """获取用户提醒"""
    reminders = get_reminders(user_id)
    return {"reminders": reminders}

@app.post("/api/reminder/{user_id}")
async def create_reminder(
    user_id: str,
    title: str,
    content: str,
    reminder_type: str = "fixed",
    time: str = "09:00"
):
    """创建提醒"""
    reminder = add_reminder(user_id, title, content, reminder_type, time)
    return {"message": "创建成功", "reminder": reminder}

@app.delete("/api/reminder/{reminder_id}")
async def remove_reminder(reminder_id: str):
    """删除提醒"""
    delete_reminder(reminder_id)
    return {"message": "删除成功"}

@app.patch("/api/reminder/{reminder_id}")
async def update_reminder_status(reminder_id: str, enabled: bool):
    """更新提醒状态"""
    toggle_reminder(reminder_id, enabled)
    return {"message": "更新成功"}

# ==================== 健康检查 ====================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "随身AI伙伴服务运行中"}

# ==================== 启动 ====================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
