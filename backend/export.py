"""
数据导入导出工具
支持备份和恢复用户数据
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "memory.db"
EXPORT_DIR = "backups"

class DataExporter:
    """数据导出器"""
    
    @classmethod
    def export_user(cls, user_id: str, filepath: str = None):
        """导出用户数据"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # 获取用户信息
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = dict(c.fetchone()) if c.fetchone() else None
        
        # 获取记忆
        c.execute("SELECT * FROM memories WHERE user_id = ?", (user_id,))
        memories = [dict(row) for row in c.fetchall()]
        
        # 获取提醒
        c.execute("SELECT * FROM reminders WHERE user_id = ?", (user_id,))
        reminders = [dict(row) for row in c.fetchall()]
        
        conn.close()
        
        data = {
            "export_time": datetime.now().isoformat(),
            "user": user,
            "memories": memories,
            "reminders": reminders
        }
        
        if not filepath:
            filepath = f"{EXPORT_DIR}/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        Path(EXPORT_DIR).mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    @classmethod
    def import_user(cls, filepath: str):
        """导入用户数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 导入用户
        if data.get('user'):
            user = data['user']
            c.execute("""
                INSERT OR REPLACE INTO users (user_id, name, preference, emotion_state, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user['user_id'], user['name'], user['preference'], 
                   user['emotion_state'], user['created_at'], user['updated_at']))
        
        # 导入记忆
        for memory in data.get('memories', []):
            c.execute("""
                INSERT OR REPLACE INTO memories (memory_id, user_id, content, memory_type, importance, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (memory['memory_id'], memory['user_id'], memory['content'],
                  memory['memory_type'], memory['importance'],
                  memory['created_at'], memory['updated_at']))
        
        # 导入提醒
        for reminder in data.get('reminders', []):
            c.execute("""
                INSERT OR REPLACE INTO reminders (reminder_id, user_id, title, content, reminder_type, time, enabled, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (reminder['reminder_id'], reminder['user_id'], reminder['title'],
                  reminder['content'], reminder['reminder_type'], reminder['time'],
                  reminder['enabled'], reminder['created_at']))
        
        conn.commit()
        conn.close()
        
        return {
            "user": data.get('user', {}).get('user_id'),
            "memories": len(data.get('memories', [])),
            "reminders": len(data.get('reminders', []))
        }
    
    @classmethod
    def export_all(cls):
        """导出所有用户数据"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT user_id FROM users")
        users = [row[0] for row in c.fetchall()]
        
        conn.close()
        
        results = []
        for user_id in users:
            filepath = cls.export_user(user_id)
            results.append({"user_id": user_id, "filepath": filepath})
        
        return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python export.py export <user_id>   导出用户数据")
        print("  python export.py import <file>     导入用户数据")
        print("  python export.py export_all       导出所有用户")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "export":
        user_id = sys.argv[2] if len(sys.argv) > 2 else "default"
        filepath = DataExporter.export_user(user_id)
        print(f"已导出到: {filepath}")
    
    elif command == "import":
        filepath = sys.argv[2] if len(sys.argv) > 2 else None
        if not filepath:
            print("请指定导入文件")
            sys.exit(1)
        result = DataExporter.import_user(filepath)
        print(f"导入成功: {result}")
    
    elif command == "export_all":
        results = DataExporter.export_all()
        print(f"已导出 {len(results)} 个用户")
        for r in results:
            print(f"  {r['user_id']}: {r['filepath']}")
    
    else:
        print(f"未知命令: {command}")
