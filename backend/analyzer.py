"""
日志分析工具
分析对话日志，提取有价值的信息
"""
import sqlite3
import json
from datetime import datetime, timedelta
from collections import Counter

DB_PATH = "memory.db"

class LogAnalyzer:
    """日志分析器"""
    
    @classmethod
    def analyze_user(cls, user_id: str, days: int = 7):
        """分析用户行为"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 获取最近N天的记忆
        since = (datetime.now() - timedelta(days=days)).isoformat()
        c.execute("""
            SELECT * FROM memories 
            WHERE user_id = ? AND created_at > ?
            ORDER BY created_at DESC
        """, (user_id, since))
        
        memories = [dict(row) for row in c.fetchall()]
        
        # 统计记忆类型
        memory_types = Counter([m['memory_type'] for m in memories])
        
        # 获取提醒统计
        c.execute("SELECT * FROM reminders WHERE user_id = ?", (user_id,))
        reminders = [dict(row) for row in c.fetchall()]
        
        conn.close()
        
        return {
            "user_id": user_id,
            "analysis_period_days": days,
            "total_memories": len(memories),
            "memory_types": dict(memory_types),
            "total_reminders": len(reminders),
            "active_reminders": len([r for r in reminders if r.get('enabled', False)]),
            "recent_memories": memories[:10]
        }
    
    @classmethod
    def get_top_memories(cls, user_id: str, limit: int = 10):
        """获取最重要的记忆"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
            SELECT * FROM memories 
            WHERE user_id = ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        memories = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return memories
    
    @classmethod
    def get_memory_timeline(cls, user_id: str):
        """获取记忆时间线"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
            SELECT date(created_at) as date, COUNT(*) as count
            FROM memories
            WHERE user_id = ?
            GROUP BY date(created_at)
            ORDER BY date DESC
            LIMIT 30
        """, (user_id,))
        
        timeline = [{"date": row[0], "count": row[1]} for row in c.fetchall()]
        conn.close()
        
        return timeline
    
    @classmethod
    def generate_report(cls, user_id: str):
        """生成用户分析报告"""
        analysis = cls.analyze_user(user_id)
        top_memories = cls.get_top_memories(user_id)
        timeline = cls.get_memory_timeline(user_id)
        
        report = f"""
# 用户分析报告

## 概览

- 用户ID: {user_id}
- 分析周期: 最近{analysis['analysis_period_days']}天
- 记忆总数: {analysis['total_memories']}
- 提醒总数: {analysis['total_reminders']}
- 活跃提醒: {analysis['active_reminders']}

## 记忆类型分布

"""
        
        for mem_type, count in analysis['memory_types'].items():
            report += f"- {mem_type}: {count}\n"
        
        report += """
## 重要记忆 (Top 10)

"""
        
        for i, mem in enumerate(top_memories, 1):
            report += f"{i}. {mem['content']} (重要性: {mem['importance']})\n"
        
        report += """
## 记忆时间线

"""
        
        for t in timeline[:10]:
            report += f"- {t['date']}: {t['count']}条记忆\n"
        
        return report


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        user_id = "default"
    else:
        user_id = sys.argv[1]
    
    report = LogAnalyzer.generate_report(user_id)
    print(report)
