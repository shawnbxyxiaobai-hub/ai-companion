"""
记忆系统模块
负责存储和检索用户记忆
"""
import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Optional

DB_PATH = "memory.db"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT DEFAULT '用户',
        preference TEXT DEFAULT '{}',
        emotion_state TEXT DEFAULT 'neutral',
        created_at TEXT,
        updated_at TEXT
    )''')
    
    # 记忆表
    c.execute('''CREATE TABLE IF NOT EXISTS memories (
        memory_id TEXT PRIMARY KEY,
        user_id TEXT,
        content TEXT,
        memory_type TEXT,
        importance INTEGER DEFAULT 3,
        created_at TEXT,
        updated_at TEXT
    )''')
    
    conn.commit()
    conn.close()

def get_user(user_id: str) -> dict:
    """获取用户信息"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            "user_id": row[0],
            "name": row[1],
            "preference": json.loads(row[2]),
            "emotion_state": row[3],
            "created_at": row[4],
            "updated_at": row[5]
        }
    return None

def create_user(user_id: str, name: str = "用户") -> dict:
    """创建用户"""
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (user_id, name, preference, emotion_state, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, name, "{}", "neutral", now, now)
    )
    conn.commit()
    conn.close()
    return get_user(user_id)

def add_memory(user_id: str, content: str, memory_type: str, importance: int = 3) -> dict:
    """添加记忆"""
    memory_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO memories (memory_id, user_id, content, memory_type, importance, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (memory_id, user_id, content, memory_type, importance, now, now)
    )
    conn.commit()
    conn.close()
    
    return {
        "memory_id": memory_id,
        "user_id": user_id,
        "content": content,
        "memory_type": memory_type,
        "importance": importance,
        "created_at": now,
        "updated_at": now
    }

def get_memories(user_id: str, memory_type: str = None) -> List[dict]:
    """获取用户记忆"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if memory_type:
        c.execute("SELECT * FROM memories WHERE user_id = ? AND memory_type = ? ORDER BY importance DESC", 
                 (user_id, memory_type))
    else:
        c.execute("SELECT * FROM memories WHERE user_id = ? ORDER BY importance DESC", (user_id,))
    
    rows = c.fetchall()
    conn.close()
    
    memories = []
    for row in rows:
        memories.append({
            "memory_id": row[0],
            "user_id": row[1],
            "content": row[2],
            "memory_type": row[3],
            "importance": row[4],
            "created_at": row[5],
            "updated_at": row[6]
        })
    return memories

def update_emotion(user_id: str, emotion_state: str):
    """更新用户情绪状态"""
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET emotion_state = ?, updated_at = ? WHERE user_id = ?", 
              (emotion_state, now, user_id))
    conn.commit()
    conn.close()

# 初始化数据库
init_db()
