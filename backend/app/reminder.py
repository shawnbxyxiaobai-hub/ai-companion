"""
提醒模块
智能提醒功能
"""
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

DB_PATH = "memory.db"
scheduler = BackgroundScheduler()

def init_reminder_db():
    """初始化提醒表"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
        reminder_id TEXT PRIMARY KEY,
        user_id TEXT,
        title TEXT,
        content TEXT,
        reminder_type TEXT,
        time TEXT,
        enabled INTEGER DEFAULT 1,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

def add_reminder(user_id: str, title: str, content: str, reminder_type: str, time: str) -> dict:
    """添加提醒"""
    reminder_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reminders (reminder_id, user_id, title, content, reminder_type, time, enabled, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (reminder_id, user_id, title, content, reminder_type, time, 1, now)
    )
    conn.commit()
    conn.close()
    
    return {
        "reminder_id": reminder_id,
        "user_id": user_id,
        "title": title,
        "content": content,
        "reminder_type": reminder_type,
        "time": time,
        "enabled": True,
        "created_at": now
    }

def get_reminders(user_id: str) -> List[dict]:
    """获取用户的所有提醒"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM reminders WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    
    reminders = []
    for row in rows:
        reminders.append({
            "reminder_id": row[0],
            "user_id": row[1],
            "title": row[2],
            "content": row[3],
            "reminder_type": row[4],
            "time": row[5],
            "enabled": bool(row[6]),
            "created_at": row[7]
        })
    return reminders

def delete_reminder(reminder_id: str):
    """删除提醒"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM reminders WHERE reminder_id = ?", (reminder_id,))
    conn.commit()
    conn.close()

def toggle_reminder(reminder_id: str, enabled: bool):
    """切换提醒状态"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE reminders SET enabled = ? WHERE reminder_id = ?", (int(enabled), reminder_id))
    conn.commit()
    conn.close()

# 初始化
init_reminder_db()
